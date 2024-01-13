import gzip
import uuid
from contextlib import asynccontextmanager, contextmanager
from enum import Enum
from io import BytesIO
from logging import error
from tempfile import TemporaryFile
from typing import (
    IO,
    Generic,
    Type,
)
from urllib.parse import urlparse

import brotli
from botocore.exceptions import ClientError

from lassen.aws import assume_aws_credentials
from lassen.store.base import (
    CreateSchemaType,
    ModelType,
    StoreCommonBase,
    UpdateSchemaType,
)


class CompressionType(Enum):
    RAW = "RAW"
    BROTLI = "BROTLI"
    GZIP = "GZIP"


class StorageBackendType(Enum):
    DISK = "DISK"
    MEMORY = "MEMORY"


COMPRESSION_TO_EXTENSION = {
    CompressionType.RAW: "",
    CompressionType.BROTLI: ".br",
    CompressionType.GZIP: ".gz",
}


class StoreS3Mixin(
    StoreCommonBase[ModelType], Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):
    pointer_attribute: str
    pointer_compression: CompressionType = CompressionType.RAW
    pointer_storage_backend: StorageBackendType = StorageBackendType.MEMORY

    # If using brotli compression, override the default level of compression
    # to balance compression speed and compression ratio
    pointer_compression_brotli_level: int = 11

    # Key prefix, including the s3:// prefix
    # If you need a dynamic override you can also make a @property of
    # your child class
    # The key suffix is usually the type of file
    key_prefix: str = ""
    key_suffix: str = ""

    def __init__(self, model: Type[ModelType]):
        super().__init__(model)

    @asynccontextmanager
    async def get_stream_from_pointer(
        self,
        obj: ModelType,
    ):
        pointer_col = self.attribute_from_key(self.pointer_attribute)
        s3_path = getattr(obj, pointer_col.name)
        if not s3_path:
            raise ValueError(f"Page element pointer does not have {pointer_col.name}")

        s3_parsed = urlparse(s3_path)

        new_session = await assume_aws_credentials()
        async with new_session.client("s3") as s3:
            try:
                raw_contents = await s3.get_object(
                    Bucket=s3_parsed.netloc,
                    Key=s3_parsed.path.strip("/"),
                )
                with self.get_output_io() as output_file:
                    # While strictly speaking the in-memory backend approaches could
                    # read the whole blob into memory at once, to keep the logic
                    # simpler we do a streaming read here to avoid bringing everything
                    # into memory for the disk backend.
                    buffer_size = 24 * 1024
                    while True:
                        chunk = await raw_contents["Body"].read(buffer_size)
                        if not chunk:
                            break
                        output_file.write(chunk)
                    output_file.seek(0)
                    with self.unwrap_compressed_file(output_file) as decompressed_file:
                        yield decompressed_file

            except ClientError as e:
                error(f"Error encountered when accessing {s3_path}: {e}")
                raise

    async def put_content_into_pointer(
        self,
        element_stub: CreateSchemaType | UpdateSchemaType,
        *,
        payload: IO[bytes],
        content_type: str | None = None,
        explicit_s3_path: str | None = None,
    ):
        """

        :param content_type: Used by S3 if serving the file from the content
            bucket. This lets browser assume the right MIME type of the
            displayed content.
        :param explicit_s3_path: In some cases clients may need to override
            the generation of the S3 path to enforce object-conditioned logic.
            If this is provided, we will ignore the key_prefix, key_suffix,
            and automatic compression extension. You're all on your own.

        """
        # Validate that our key prefix is valid
        if not self.key_prefix.startswith("s3://"):
            raise ValueError(f"Key prefix '{self.key_prefix}' must start with s3://")

        # We assume that we should follow the store-based preferences for both
        # the compression and the backend type
        with self.wrap_compressed_file(payload) as compressed_payload:
            # Guess the additional suffix that is required based on the extension
            # and the compression type
            compressed_extension = (
                self.key_suffix + COMPRESSION_TO_EXTENSION[self.pointer_compression]
            )

            return await self.copy_content_into_pointer(
                element_stub,
                payload=compressed_payload,
                extension=compressed_extension,
                content_type=content_type,
                explicit_s3_path=explicit_s3_path,
            )

    async def copy_content_into_pointer(
        self,
        element_stub: CreateSchemaType | UpdateSchemaType,
        *,
        payload: IO[bytes],
        extension: str,
        content_type: str | None = None,
        explicit_s3_path: str | None = None,
    ):
        """
        Puts the raw content into the S3 bucket. The only time clients should
        call this manually is if you need to perform your compression manually.
        Otherwise we have better default handling in `put_content_into_pointer`.

        """
        s3_metadata_path = (
            f"{self.key_prefix}/{uuid.uuid4()}{extension}"
            if not explicit_s3_path
            else explicit_s3_path
        )
        s3_parsed = urlparse(s3_metadata_path)

        optional_args = (
            {
                "ContentType": content_type,
            }
            if content_type
            else {}
        )

        new_session = await assume_aws_credentials()
        async with new_session.client("s3") as s3:
            try:
                await s3.upload_fileobj(
                    Bucket=s3_parsed.netloc,
                    Key=s3_parsed.path.strip("/"),
                    Fileobj=payload,
                    **optional_args,
                )
            except ClientError as e:
                error(f"Error encountered when accessing {s3_metadata_path}: {e}")
                raise

        setattr(element_stub, self.pointer_attribute, s3_metadata_path)
        return element_stub

    @contextmanager
    def wrap_compressed_file(self, file: IO[bytes], buffer_size=24 * 1024):
        if self.pointer_compression == CompressionType.RAW:
            yield file
        elif self.pointer_compression == CompressionType.BROTLI:
            compressor = brotli.Compressor(
                quality=self.pointer_compression_brotli_level,
            )
            with self.get_output_io() as output_file:
                while True:
                    chunk = file.read(buffer_size)
                    if not chunk:
                        break
                    output_file.write(compressor.process(chunk))
                output_file.write(compressor.finish())
                output_file.seek(0)
                yield output_file
        elif self.pointer_compression == CompressionType.GZIP:
            with self.get_output_io() as output_file:
                with gzip.GzipFile(fileobj=output_file, mode="wb") as compressor:
                    while True:
                        chunk = file.read(buffer_size)
                        if not chunk:
                            break
                        compressor.write(chunk)
                output_file.seek(0)
                yield output_file
        else:
            raise ValueError(f"Unknown compression type {self.pointer_compression}")

    @contextmanager
    def unwrap_compressed_file(self, file: IO[bytes], buffer_size=24 * 1024):
        if self.pointer_compression == CompressionType.RAW:
            yield file
        elif self.pointer_compression == CompressionType.BROTLI:
            decompressor = brotli.Decompressor()
            with self.get_output_io() as output_file:
                while True:
                    chunk = file.read(buffer_size)
                    if not chunk:
                        break
                    output_file.write(decompressor.process(chunk))
                output_file.seek(0)
                yield output_file
        elif self.pointer_compression == CompressionType.GZIP:
            with self.get_output_io() as output_file:
                with gzip.GzipFile(fileobj=file, mode="rb") as decompressor:
                    while True:
                        chunk = decompressor.read(buffer_size)
                        if not chunk:
                            break
                        output_file.write(chunk)
                output_file.seek(0)
                yield output_file
        else:
            raise ValueError(f"Unknown compression type {self.pointer_compression}")

    @contextmanager
    def get_output_io(self):
        if self.pointer_storage_backend == StorageBackendType.DISK:
            with TemporaryFile() as output_file:
                yield output_file
        elif self.pointer_storage_backend == StorageBackendType.MEMORY:
            yield BytesIO()
        else:
            raise ValueError(f"Unknown storage backend {self.pointer_storage_backend}")
