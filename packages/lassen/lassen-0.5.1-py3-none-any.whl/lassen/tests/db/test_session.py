from lassen.db.session import get_db_context
from lassen.tests.model_fixtures import SampleModel


def test_commit(db_session):
    with get_db_context() as db:
        new_user = SampleModel(name="john")
        db.add(new_user)

    with get_db_context() as db:
        fetched_user = db.query(SampleModel).filter_by(name="john").first()
        assert fetched_user is not None


def test_exception_rollback(db_session):
    saw_exception = False
    try:
        with get_db_context() as db:
            new_user = SampleModel(name="doe")
            db.add(new_user)
            raise ValueError("Triggering exception")
    except ValueError:
        saw_exception = True

    assert saw_exception

    # Validate that the user 'doe' wasn't committed due to the exception
    with get_db_context() as db_session:
        fetched_user = db_session.query(SampleModel).filter_by(name="doe").first()
        assert fetched_user is None


def test_object_refreshing(db_session):
    with get_db_context(refresh=True) as db:
        new_user = SampleModel(name="mark")
        db.add(new_user)

    # Validate that the object has an ID (refreshed)
    assert new_user.id is not None


def test_skips_update_on_delete(db_session):
    with get_db_context() as db:
        new_user = SampleModel(name="mark")
        db.add(new_user)
        db.flush()

        assert db.already_flushed_objects == {new_user}

        # Now delete the element
        db.delete(new_user)
        db.flush()

        assert db.already_deleted_objects == {new_user}


def test_skips_update_on_concurrent_delete(db_session):
    with get_db_context() as db_main:
        new_user = SampleModel(name="mark")
        db_main.add(new_user)
        db_main.commit()
        db_main.refresh(new_user)

        # The object is now created and has an id
        assert db_main.already_flushed_objects == {new_user}

        with get_db_context() as db_background:
            # Now delete the element
            new_user_background = (
                db_background.query(SampleModel).filter_by(id=new_user.id).first()
            )
            db_background.delete(new_user_background)

        # The object is now deleted but the main session doesn't know it yet
        assert db_main.already_flushed_objects == {new_user}

    # We expect that the context will close and the cleanup will skip over
    # the deleted object
    assert True


def test_get_attribute_after_scope(db_session):
    with get_db_context() as db_main:
        new_user = SampleModel(name="mark")
        db_main.add(new_user)

    assert new_user.name == "mark"
