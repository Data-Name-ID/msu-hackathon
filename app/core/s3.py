from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, BinaryIO
from uuid import uuid4

from aiobotocore.session import get_session

from app.core.store import Store


class S3Accessor:
    def __init__(self, store: Store) -> None:
        self.store = store

        self.endpoint = store.config.s3.endpoint
        self.secret_key = store.config.s3.secret_key
        self.access_key = store.config.s3.access_key
        self.bucket = store.config.s3.bucket

        self.session = get_session()

    @asynccontextmanager
    async def create_client(self) -> AsyncGenerator[Any, None]:
        async with self.session.create_client(
            "s3",
            endpoint_url=self.endpoint,
            aws_secret_access_key=self.secret_key,
            aws_access_key_id=self.access_key,
        ) as client:
            yield client

    async def put(self, file: BinaryIO, path: str, filename: str) -> str:
        suffix = Path(filename).suffix
        key = f"{path}/{uuid4().hex}{suffix}"

        async with self.create_client() as client:
            await client.put_object(Bucket=self.bucket, Key=key, Body=file)
            return f"{self.endpoint}/{self.bucket}/{key}"

    async def delete(self, url: str) -> None:
        key = url.removeprefix(f"{self.endpoint}/{self.bucket}/")
        async with self.create_client() as client:
            await client.delete_object(Bucket=self.bucket, Key=key)
