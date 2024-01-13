from contextlib import asynccontextmanager
from json import dumps as json_dumps
from os import environ
from tempfile import TemporaryDirectory
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy import text

from lassen.core.config import CoreSettings, register_settings
from lassen.db.session import get_db_context
from lassen.tests.conftest_helpers.aws import MockAWS, MockLambdaClient, MockS3Client


@pytest.fixture(autouse=True, scope="session")
def inject_env_variables():
    """
    Inject fake environment variables for testing purposes.

    """
    settings = CoreSettings(
        BACKEND_CORS_ORIGINS=["http://localhost"],
        SERVER_NAME="lassen-test",
        POSTGRES_SERVER="localhost",
        POSTGRES_USER="lassen",
        POSTGRES_PASSWORD="mypassword",
        POSTGRES_DB="lassen_test_db",
    )

    # Convert settings into env variables
    for key, value in settings.model_dump().items():
        if value:
            if isinstance(value, list):
                value = json_dumps([str(val) for val in value])
            else:
                value = str(value)

            print(f"Test Env: Will set `{key}` = `{value}`")  # noqa
            environ[key] = value

    # We don't have a client-specific settings object, so we'll just back-register
    # the core settings
    register_settings(CoreSettings)


@pytest.fixture()
def clear_db():
    with get_db_context() as db:
        # Drop the alembic specific tables
        db.execute(text("DROP TABLE IF EXISTS alembic_version"))

        # Commit these changes
        db.execute(text("COMMIT"))

    with get_db_context() as db:
        # Import all models used in tests
        import lassen.tests.fixtures.test_harness.test_harness.models  # noqa
        import lassen.tests.model_fixtures  # noqa

        # Make sure each test has a fresh context
        from lassen.db.base_class import Base

        Base.metadata.drop_all(bind=db.bind)


@pytest.fixture()
def db_session(clear_db):
    # Because this is scoped to the whole test function, refreshes would be run
    # after the test is completed. We set to false to save on some performance time
    # seeing as this isn't otherwise needed.
    with get_db_context(refresh=False) as db:
        # Import all models used in tests
        import lassen.tests.fixtures.test_harness.test_harness.models  # noqa
        import lassen.tests.model_fixtures  # noqa

        from lassen.db.base_class import Base

        Base.metadata.create_all(bind=db.bind)

        yield db


@pytest.fixture()
def tempdir():
    with TemporaryDirectory() as tempdir:
        yield tempdir


@pytest.fixture
def mock_aws():
    """
    Mock the S3 client so we can test the S3 storage backend
    """
    mock_aws = MockAWS(
        mock_s3=MockS3Client(
            whitelisted_buckets=[
                "lassen-test",
            ],
        ),
        mock_lambda=MockLambdaClient(),
    )

    @asynccontextmanager
    async def mock_client(client_type: str, **kwargs):
        if client_type == "sts":
            yield AsyncMock()
        elif client_type == "s3":
            yield mock_aws.mock_s3
        elif client_type == "lambda":
            yield mock_aws.mock_lambda
        else:
            raise ValueError(f"Unknown mock client type: {client_type}")

    # Appropriate use of the session as a session contextmanager
    mock_session = MagicMock()
    mock_session.client = mock_client

    # Patch aioboto3.Session to return the mock session
    with patch("aioboto3.Session", return_value=mock_session):
        yield mock_aws
