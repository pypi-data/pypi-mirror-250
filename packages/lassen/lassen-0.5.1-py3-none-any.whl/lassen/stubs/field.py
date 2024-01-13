from typing import Any, Callable

from pydantic import BaseModel

from lassen.enums import FilterTypeEnum
from lassen.stubs.base import BaseGenerator


class UNSET_VALUE:
    pass


FieldGeneratorCustomization = list[tuple[BaseGenerator, bool]]


class FieldDefinition(BaseModel):
    description: str | None
    examples: list[Any]
    # CRUD models for visibility
    create: bool | FieldGeneratorCustomization
    update: bool | FieldGeneratorCustomization
    read: bool | FieldGeneratorCustomization
    # DB level model
    persistent: bool | FieldGeneratorCustomization
    filter: bool | FieldGeneratorCustomization
    filter_extensions: list[FilterTypeEnum] | UNSET_VALUE
    index: bool
    is_relationship: bool
    association_proxy: tuple[str, str] | UNSET_VALUE
    primary_key: bool | UNSET_VALUE
    foreign_key: Any | UNSET_VALUE
    backref: str | UNSET_VALUE
    back_populates: str | UNSET_VALUE
    default: Any | UNSET_VALUE
    db_alias: str | UNSET_VALUE

    class Config:
        arbitrary_types_allowed = True
        extra = "forbid"


def Field(
    description: str | None = None,
    examples: list[Any] | None = None,
    create: bool | FieldGeneratorCustomization = False,
    update: bool | FieldGeneratorCustomization = False,
    read: bool | FieldGeneratorCustomization = True,
    persistent: bool | FieldGeneratorCustomization = True,
    filter: bool | FieldGeneratorCustomization = False,
    filter_extensions: list[FilterTypeEnum] | UNSET_VALUE = UNSET_VALUE(),
    index: bool = False,
    is_relationship: bool = False,
    association_proxy: tuple[str, str] | UNSET_VALUE = UNSET_VALUE(),
    primary_key: bool | UNSET_VALUE = UNSET_VALUE(),
    foreign_key: Any = UNSET_VALUE(),
    backref: str | UNSET_VALUE = UNSET_VALUE(),
    back_populates: str | UNSET_VALUE = UNSET_VALUE(),
    default: Any | Callable | UNSET_VALUE = UNSET_VALUE(),
    db_alias: str | UNSET_VALUE = UNSET_VALUE(),
) -> Any:
    """
    :param generators: By default, all class-associated generators are used
    :param default: If you want to set a more complex expression as your default
        you can use a lambda x: {my value} expression. This delays execution of
        the actual logic and we'll instead use the lambda values.
    :param If set to True, enables regular equality expressions for this field.
        For additional options, see the filter_extensions parameter.
    :param filter_extensions: List of additional filter extensions
        to enable for this field.

    """
    return FieldDefinition(
        description=description,
        examples=examples or [],
        create=create,
        update=update,
        read=read,
        persistent=persistent,
        filter=filter,
        filter_extensions=filter_extensions,
        index=index,
        is_relationship=is_relationship,
        association_proxy=association_proxy,
        primary_key=primary_key,
        foreign_key=foreign_key,
        backref=backref,
        back_populates=back_populates,
        default=default,
        db_alias=db_alias,
    )
