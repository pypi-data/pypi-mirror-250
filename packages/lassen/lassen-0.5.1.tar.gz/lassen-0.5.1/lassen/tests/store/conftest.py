import pytest
from sqlalchemy.orm import Session


@pytest.fixture
def use_fixture_models(db_session: Session):
    if not db_session.bind:
        raise ValueError("No database connection")

    from lassen.db.base_class import Base

    Base.metadata.create_all(bind=db_session.bind)
