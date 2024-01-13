import io
from itertools import product
from unittest.mock import patch

import pytest
from boto3 import Session

from lassen.store.base import StoreBase
from lassen.store.s3 import CompressionType, StorageBackendType, StoreS3Mixin
from lassen.tests.conftest_helpers.aws import MockAWS
from lassen.tests.model_fixtures import (
    SampleModel,
    SampleSchemaCreate,
    SampleSchemaUpdate,
)


@pytest.mark.parametrize(
    "compression_type,backend_type,data_size",
    list(
        product(
            [CompressionType.RAW, CompressionType.BROTLI, CompressionType.GZIP],
            [StorageBackendType.DISK, StorageBackendType.MEMORY],
            [0, 1024, 50 * 1024],
        )
    ),
)
def test_compression_decompression(
    compression_type: CompressionType,
    backend_type: StorageBackendType,
    data_size: int,
    db_session: Session,
    use_fixture_models,
    mock_aws,
):
    original_data = b"x" * data_size

    class ExampleS3Store(
        StoreS3Mixin[SampleModel, SampleSchemaCreate, SampleSchemaUpdate]
    ):
        pointer_attribute = "s3_path"
        pointer_compression = compression_type
        pointer_storage_backend = backend_type
        key_prefix = "s3://lassen-test/test-prefix"

    stub_s3 = ExampleS3Store(SampleModel)

    with io.BytesIO(original_data) as file:
        with stub_s3.wrap_compressed_file(file) as compressed_file:
            compressed_data = compressed_file.read()

            with io.BytesIO(compressed_data) as compressed_io:
                with stub_s3.unwrap_compressed_file(compressed_io) as decompressed_file:
                    decompressed_data = decompressed_file.read()

    assert original_data == decompressed_data


@pytest.mark.parametrize("invalid_compression_type", ["INVALID_TYPE", None, 123])
def test_invalid_compression_type(
    invalid_compression_type,
    db_session: Session,
    use_fixture_models,
    mock_aws,
):
    class ExampleS3Store(
        StoreS3Mixin[SampleModel, SampleSchemaCreate, SampleSchemaUpdate]
    ):
        pointer_attribute = "s3_path"
        pointer_compression = invalid_compression_type
        pointer_storage_backend = StorageBackendType.DISK
        key_prefix = "s3://lassen-test/test-prefix"

    stub_s3 = ExampleS3Store(SampleModel)

    with pytest.raises(ValueError):
        with io.BytesIO(b"test data") as file:
            with stub_s3.wrap_compressed_file(file) as _:
                pass


@pytest.mark.asyncio
async def test_s3_upload(mock_aws: MockAWS):
    """
    Ensure that we can properly upload and download data to S3. This test does not
    need to be fully parameterized with the different encoding and storage options
    because these are tested separately.

    """

    class ExampleS3Store(
        StoreS3Mixin[SampleModel, SampleSchemaCreate, SampleSchemaUpdate]
    ):
        pointer_attribute = "s3_path"
        pointer_compression = CompressionType.RAW
        pointer_storage_backend = StorageBackendType.MEMORY
        key_prefix = "s3://lassen-test/test-prefix"

    stub_s3 = ExampleS3Store(SampleModel)

    with patch("uuid.uuid4", return_value="test-uuid"):
        create_stub = await stub_s3.put_content_into_pointer(
            SampleSchemaCreate(name="test"),
            payload=io.BytesIO(b"test data"),
        )

    # We have retained the passed-in properties and added our s3 path
    # to the appropriate attribute
    assert create_stub.name == "test"
    assert create_stub.s3_path == "s3://lassen-test/test-prefix/test-uuid"

    # Make sure we have actually written this path to S3
    obj = await mock_aws.mock_s3.get_object(
        Bucket="lassen-test",
        Key="test-prefix/test-uuid",
    )
    assert await obj["Body"].read() == b"test data"


@pytest.mark.asyncio
async def test_s3_download(db_session: Session, use_fixture_models, mock_aws: MockAWS):
    class ExampleS3Store(
        StoreBase[SampleModel, SampleSchemaCreate, SampleSchemaUpdate],
        StoreS3Mixin[SampleModel, SampleSchemaCreate, SampleSchemaUpdate],
    ):
        pointer_attribute = "s3_path"
        pointer_compression = CompressionType.RAW
        pointer_storage_backend = StorageBackendType.MEMORY
        key_prefix = "s3://lassen-test/test-prefix"

    stub_s3 = ExampleS3Store(SampleModel)

    # Manually upload a file to S3 and create the database object
    await mock_aws.mock_s3.put_object(
        Bucket="lassen-test",
        Key="test-prefix/test-uuid",
        Body=b"test data",
    )

    db_obj = stub_s3.create(
        db_session,
        obj_in=SampleSchemaCreate(
            name="test", s3_path="s3://lassen-test/test-prefix/test-uuid"
        ),
    )

    # Make sure we can download the file
    async with stub_s3.get_stream_from_pointer(db_obj) as file:
        assert file.read() == b"test data"


@pytest.mark.asyncio
async def test_explicit_s3_key(
    db_session: Session, use_fixture_models, mock_aws: MockAWS
):
    class ExampleS3Store(
        StoreBase[SampleModel, SampleSchemaCreate, SampleSchemaUpdate],
        StoreS3Mixin[SampleModel, SampleSchemaCreate, SampleSchemaUpdate],
    ):
        pointer_attribute = "s3_path"
        pointer_compression = CompressionType.RAW
        pointer_storage_backend = StorageBackendType.MEMORY
        key_prefix = "s3://lassen-test/test-prefix"

    stub_s3 = ExampleS3Store(SampleModel)

    # Manually upload a file to S3 and create the database object
    await stub_s3.put_content_into_pointer(
        SampleSchemaCreate(
            name="test",
        ),
        payload=io.BytesIO(b"test data"),
        explicit_s3_path="s3://lassen-test/test-prefix/test-uuid",
    )

    # Get the file from where we expect in S3
    obj = await mock_aws.mock_s3.get_object(
        Bucket="lassen-test",
        Key="test-prefix/test-uuid",
    )
    assert await obj["Body"].read() == b"test data"
