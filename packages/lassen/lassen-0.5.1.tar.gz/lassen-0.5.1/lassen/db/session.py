import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import Session, sessionmaker

from lassen.core.config import get_settings

SessionLocal: sessionmaker[Session] | None = None


class LassenDBSession(Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.already_flushed_objects = set()
        self.already_deleted_objects = set()

    def register_modified_objects(self):
        """
        Before flush or commit, we should cache the modified objects
        locally. Flushes by default will clear these out of the in-memory cache.

        """
        self.already_flushed_objects |= set(self.new).union(self.dirty)
        self.already_deleted_objects |= set(self.deleted)

    def flush(self, *args, **kwargs):
        self.register_modified_objects()
        return super().flush(*args, **kwargs)

    def commit(self, *args, **kwargs):
        self.register_modified_objects()
        return super().commit(*args, **kwargs)


def get_session_local():
    global SessionLocal
    if SessionLocal is not None:
        return SessionLocal

    settings = get_settings()
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), pool_pre_ping=True)
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=LassenDBSession,
        expire_on_commit=False,
    )
    return SessionLocal


@contextmanager
def get_db_context(refresh: bool = False):
    """
    Context manager for database sessions. This will create a new session scope
    with a transaction and commit on exit. If an exception is raised, the whole
    transaction will be rolled back. Clients should use one context manager for
    any scope that is likely to crash and might result in partial objects.

    :param refresh: If True, refreshes all objects after commit. This is useful
        to get IDs, etc. for objects that were created in the session. Note that
        this is a best effort refresh; if we are unable to refresh an object (perhaps
        because the remote database side has changed in the meantime) we will skip
        it silently and continue for the other session objects.

    """
    db: LassenDBSession | None = None
    try:
        db = get_session_local()()

        # We expect to always get a database session, but mypy throws
        # an error that Session|None is not compatible with the Session
        # specific attributes. This is mainly a workaround but also
        # probably worth validating explicitly.
        if not db:
            raise ValueError("No database session found")
        yield db

        db.commit()

        if refresh:
            # Refreshing all new or modified objects to get IDs, etc.
            for obj in db.already_flushed_objects:
                # Skip deleted objects
                if obj not in db.already_deleted_objects:
                    try:
                        db.refresh(obj)
                    except InvalidRequestError:
                        # Object was likely deleted, or for some other reason
                        # can't be refreshed
                        pass
        db.already_flushed_objects.clear()
        db.already_deleted_objects.clear()
    except Exception as e:
        # Rolling back in case of exception
        if db is not None:
            db.rollback()
        logging.error(f"An error occurred in the db context, rolling back: {e}")
        # Re-raise the caught exception
        raise
    finally:
        if db is not None:
            db.close()
