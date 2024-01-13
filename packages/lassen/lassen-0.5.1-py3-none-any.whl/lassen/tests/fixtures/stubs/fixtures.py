from datetime import datetime
from enum import Enum

from lassen.stubs.base import BaseStub
from lassen.stubs.field import Field
from lassen.stubs.generators import SchemaGenerator, StoreGenerator


class SimpleEnum(Enum):
    TEST = "TEST"


class UserStub(BaseStub):
    store_gen = StoreGenerator("stores")
    schema_gen = SchemaGenerator("schemas")
    public_schema_gen = SchemaGenerator("schemas_public")

    first_name: str = Field(description="First name of the user", examples=["John"])
    last_name: str | None = Field(description="Last name of the user", examples=["Smith"])

    password: str = Field(create=True)

    enum_value: SimpleEnum = Field(
        read=[(store_gen, True), (schema_gen, True), (public_schema_gen, False)]
    )

    creation_date: datetime = Field(
        default=lambda: datetime.now(),
        read=[(store_gen, True), (schema_gen, True), (public_schema_gen, False)]
    )
