"""
Simple stub utilities to test AWS plugins.

"""
from dataclasses import dataclass
from json import dumps as json_dumps
from typing import IO, Any


class MockReadableObject:
    def __init__(self, content: bytes):
        self.content = content
        self.current_position = 0

    async def read(self, chunk_size: int = -1):
        if chunk_size == -1:
            chunk_size = len(self.content) - self.current_position
        chunk = self.content[self.current_position : self.current_position + chunk_size]
        self.current_position += len(chunk)
        return chunk


class MockS3Client:
    def __init__(self, whitelisted_buckets: list[str] = []):
        self.cache: dict[tuple[str, str], Any] = {}
        self.whitelisted_buckets = whitelisted_buckets

    async def put_object(self, Bucket: str, Key: str, Body: str | bytes, **kwargs):
        if Bucket not in self.whitelisted_buckets:
            raise ValueError(f"Bucket not whitelisted: {Bucket}")

        # Data is stored as bytes, so convert if necessary
        self.cache[(Bucket, Key)] = Body if isinstance(Body, bytes) else Body.encode()

    async def upload_fileobj(
        self, Bucket: str, Key: str, Fileobj: IO[bytes] | IO[str], **kwargs
    ):
        if Bucket not in self.whitelisted_buckets:
            raise ValueError(f"Bucket not whitelisted: {Bucket}")

        # Data is stored as bytes, so convert if necessary
        contents = Fileobj.read()
        self.cache[(Bucket, Key)] = (
            contents if isinstance(contents, bytes) else contents.encode()
        )

    async def delete_object(self, Bucket: str, Key: str):
        if Bucket not in self.whitelisted_buckets:
            raise ValueError(f"Bucket not whitelisted: {Bucket}")

        if (Bucket, Key) in self.cache:
            del self.cache[(Bucket, Key)]

    async def get_object(self, Bucket: str, Key: str, **kwargs):
        if Bucket not in self.whitelisted_buckets:
            raise ValueError(f"Bucket not whitelisted: {Bucket}")

        if (Bucket, Key) in self.cache:

            def read_object():
                return self.cache[(Bucket, Key)]

            return {"Body": MockReadableObject(self.cache[(Bucket, Key)])}
        else:
            raise Exception(f"Object not found: mocked-s3://{Bucket}/{Key}")


class MockLambdaClient:
    def __init__(self) -> None:
        self.read_value: dict[str, Any] | None = None

    async def invoke(self, *args, **kwargs):
        if not self.read_value:
            raise ValueError("Lambda value has not been set")

        return {
            "StatusCode": 200,
            "Payload": MockReadableObject(json_dumps(self.read_value).encode()),
        }


@dataclass
class MockAWS:
    mock_s3: MockS3Client
    mock_lambda: MockLambdaClient
