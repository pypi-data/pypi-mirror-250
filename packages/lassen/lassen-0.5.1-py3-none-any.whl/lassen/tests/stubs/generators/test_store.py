import datetime
from enum import Enum
from typing import Any, Dict, List, get_type_hints
from uuid import UUID

import pytest
import sqlalchemy
from pydantic import BaseModel

from lassen.db.columns import LassenUUID
from lassen.stubs.base import BaseStub
from lassen.stubs.common import ExtractedStubImports
from lassen.stubs.definition import UniqueDefinition
from lassen.stubs.field import Field
from lassen.stubs.generators.store import DEFAULT_ORIGIN_MAPPING, StoreGenerator


class SimpleEnum(Enum):
    TEST = "TEST"


class SimplePydanticModel(BaseModel):
    TEST: str


class OtherModel(BaseStub):
    pass


class MyParentModel(BaseStub):
    children: list["MyChildModel"] = Field(is_relationship=True, backref="user_parent")


class MyChildModel(BaseStub):
    user_parent_id: int = Field(foreign_key="my_parent_model.id")
    user_parent: "MyParentModel" = Field(
        foreign_key=user_parent_id, is_relationship=True
    )


@pytest.mark.parametrize(
    "typehint, expected_str, expected_class",
    [
        (int, "Integer()", sqlalchemy.Integer()),
        (float, "Float()", sqlalchemy.Float()),
        (SimpleEnum, "Enum(SimpleEnum)", sqlalchemy.Enum(SimpleEnum)),
        (list[str], "ARRAY(String())", sqlalchemy.ARRAY(sqlalchemy.String())),
        (List[str], "ARRAY(String())", sqlalchemy.ARRAY(sqlalchemy.String())),
        (str | None, "String()", sqlalchemy.String()),
        (Any, "JSON()", sqlalchemy.JSON()),
        (dict[str, str], "JSON()", sqlalchemy.JSON()),
        (Dict[str, str], "JSON()", sqlalchemy.JSON()),
        (SimplePydanticModel, "JSON()", sqlalchemy.JSON()),
        (list[SimplePydanticModel], "JSON()", sqlalchemy.JSON()),
        (UUID, "LassenUUID(as_uuid=True)", LassenUUID()),
        (bytes, "LargeBinary()", sqlalchemy.LargeBinary()),
    ],
)
def test_format_column_for_sqlalchemy(typehint, expected_str, expected_class):
    store_generator = StoreGenerator("test")
    (
        formatted_column,
        class_value,
        dependencies,
    ) = store_generator.format_column_for_sqlalchemy(typehint)

    assert formatted_column == expected_str
    # Since the classes are fully instantiated separately and therefore fail exact
    # equality, compare the string values
    assert str(class_value) == str(expected_class)
    assert len(dependencies) > 0


def test_format_column_for_sqlalchemy_custom_type():
    # Assert that our custom class isn't in the default mapping, otherwise
    # this test doesn't verify the intended behavior
    assert datetime.date not in DEFAULT_ORIGIN_MAPPING

    class CustomGenerator(StoreGenerator):
        origin_mapping = {
            **DEFAULT_ORIGIN_MAPPING,
            datetime.date: sqlalchemy.Date,
        }

    store_generator = CustomGenerator("test")
    (
        formatted_column,
        class_value,
        dependencies,
    ) = store_generator.format_column_for_sqlalchemy(datetime.date)

    assert formatted_column == "Date()"
    # Since the classes are fully instantiated separately and therefore fail
    # exact equality, compare the string values
    assert str(class_value) == str(sqlalchemy.Date())
    assert len(dependencies) > 0


def test_generate_relationship() -> None:
    store_generator = StoreGenerator("test")
    definition = store_generator(
        MyChildModel, ExtractedStubImports([], []), get_type_hints(MyChildModel)
    )

    assert (
        "user_parent_id: Mapped[int] = mapped_column(ForeignKey('my_parent_model.id'))"
        in definition.content
    )
    assert (
        "user_parent: Mapped['MyParentModel'] ="
        " relationship(foreign_keys=[user_parent_id])"
    ) in definition.content


def test_generate_one_many_relationship() -> None:
    store_generator = StoreGenerator("test")
    definition = store_generator(
        MyParentModel, ExtractedStubImports([], []), get_type_hints(MyParentModel)
    )

    assert (
        "children: Mapped[list['MyChildModel']] = relationship(backref='user_parent')"
        in definition.content
    )


def test_get_model_table_args() -> None:
    class MyModel(BaseStub):
        unique_text: str = Field()

        my_unique_constraint = UniqueDefinition(
            name="my_unique_constraint", fields=[unique_text]
        )

    store_generator = StoreGenerator("test")
    definitions, _ = store_generator.get_model_table_args(MyModel)
    assert definitions == [
        "UniqueConstraint('unique_text', name='my_unique_constraint')"
    ]
