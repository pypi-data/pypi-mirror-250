from typing import Dict, List, Optional, Union, get_type_hints

import pytest

from lassen.stubs.base import BaseStub
from lassen.stubs.common import ExtractedStubImports
from lassen.stubs.field import Field
from lassen.stubs.generators.schema import SchemaGenerator, is_optional, make_optional
from lassen.stubs.generators.store import StoreGenerator


@pytest.fixture
def schema_generator():
    # We assume we won't actually run the full generation pipeline to create
    # this path. The generator itself will only ever return text metadata; so
    # passing in a real-looking path here is okay.
    return SchemaGenerator("schemas")


@pytest.fixture
def store_generator():
    return StoreGenerator("models")


@pytest.mark.parametrize(
    "input_type, expected_output",
    [
        (int, Union[int, type(None)]),
        (int, int | None),
        (str | int, Union[str, int, type(None)]),
        (str, Union[str, type(None)]),
        (List[int], Union[List[int], type(None)]),
        (Dict[str, int], Union[Dict[str, int], type(None)]),
        (Union[int, str], Union[int, str, type(None)]),
        (Union[int, None], Union[int, None]),
        (Optional[int], Union[int, None]),
        (Optional[str], Union[str, None]),
    ],
)
def test_make_optional(input_type, expected_output):
    assert make_optional(input_type) == expected_output


@pytest.mark.parametrize(
    "input_type, expected_output",
    [
        (int, False),
        (str, False),
        (List[int], False),
        (Dict[str, int], False),
        (Union[int, str], False),
        (Union[int, None], True),
        (Optional[int], True),
        (Optional[str], True),
        (str | None, True),
    ],
)
def test_is_optional(input_type, expected_output):
    assert is_optional(input_type) == expected_output


def test_invalid_generators(
    schema_generator: SchemaGenerator,
    store_generator: StoreGenerator,
):
    """
    Parent doesn't have a store, this should be invalid to specify as a
    relationship that can be created.

    """

    class Parent(BaseStub):
        schema_gen = schema_generator

    class Child(BaseStub):
        schema_gen = schema_generator
        store_gen = store_generator

        parent: Parent = Field(
            is_relationship=True,
            backref="children",
            create=True,
        )

        parent_id: int = Field(
            is_relationship=True,
            foreign_key="parent.id",
        )

    with pytest.raises(ValueError):
        schema_generator(
            Child,
            ExtractedStubImports(clone_imports=[], clone_typechecking_imports=[]),
            get_type_hints(Child),
        )


def test_creates_db_relationship(
    schema_generator: SchemaGenerator,
    store_generator: StoreGenerator,
):
    class Parent(BaseStub):
        schema_gen = schema_generator
        store_gen = store_generator

        children: list["Child"] = Field(
            is_relationship=True,
            backref="parent",
        )

    class Child(BaseStub):
        schema_gen = schema_generator
        store_gen = store_generator

        parent: Parent = Field(
            is_relationship=True,
            backref="children",
            create=True,
        )

        parent_id: int = Field(
            is_relationship=True,
            foreign_key="parent.id",
        )

    rendered_file = schema_generator(
        Child,
        ExtractedStubImports(clone_imports=[], clone_typechecking_imports=[]),
        get_type_hints(Child),
    )

    assert "from lassen.models.parent import Parent" in rendered_file.content
    assert "parent: Parent" in rendered_file.content

    # arbitrary_types_allowed has to be enabled to allow for non-pydantic models
    # to be passed in as the relationship values
    assert "arbitrary_types_allowed=True" in rendered_file.content
