from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class SearchWrapper(BaseModel, Generic[T]):
    count: int
    limit: int
    skip: int
    items: list[T]
