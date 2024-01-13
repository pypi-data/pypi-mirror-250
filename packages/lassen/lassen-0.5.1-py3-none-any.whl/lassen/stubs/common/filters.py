import inspect
from enum import Enum
from typing import Type

from lassen.stubs.base import BaseGenerator, BaseStub
from lassen.stubs.field import UNSET_VALUE, FieldDefinition, FieldGeneratorCustomization


class ActiveFieldType(Enum):
    READ = "READ"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    FILTER = "FILTER"

    # Database backed
    PERSISTENT = "PERSISTENT"


def generator_in_field_type(
    stub: Type[BaseStub],
    generator: BaseGenerator,
    field_name: str,
    field_definition: FieldDefinition,
    field_type: ActiveFieldType,
):
    candidate_field: bool | FieldGeneratorCustomization | None = None

    if field_type == ActiveFieldType.READ:
        candidate_field = field_definition.read
    elif field_type == ActiveFieldType.CREATE:
        candidate_field = field_definition.create
    elif field_type == ActiveFieldType.UPDATE:
        candidate_field = field_definition.update
    elif field_type == ActiveFieldType.FILTER:
        candidate_field = field_definition.filter
    elif field_type == ActiveFieldType.PERSISTENT:
        candidate_field = field_definition.persistent
    else:
        raise ValueError(f"Unknown field type {field_type}")

    matches_filter = None

    if isinstance(candidate_field, bool):
        matches_filter = candidate_field
    elif isinstance(candidate_field, list):
        # Make sure that the user has specified a definition for each generator
        candidate_generators = {gen for gen, _ in candidate_field}
        defined_generators = set(stub.get_generators())
        if candidate_generators != defined_generators:
            raise ValueError(
                f"Field {stub.__name__}.{field_name} is missing generators:"
                f" {defined_generators - candidate_generators}"
            )

        for compare_generator, is_active in candidate_field:
            if generator == compare_generator:
                matches_filter = is_active

    if field_type == ActiveFieldType.FILTER:
        if not isinstance(field_definition.filter_extensions, UNSET_VALUE):
            matches_filter = True

    if matches_filter is None:
        raise ValueError(f"Unknown field value {candidate_field}")

    return matches_filter


def get_active_fields(
    stub: Type[BaseStub],
    generator: BaseGenerator,
    mask: ActiveFieldType | None = None,
):
    raw_fields: list[tuple[str, FieldDefinition]] = list(
        inspect.getmembers(stub, lambda m: isinstance(m, FieldDefinition))
    )

    if not mask:
        return raw_fields

    # Now, filter by fields that meet this mask, if specified
    return [
        (field_name, field)
        for field_name, field in raw_fields
        if generator_in_field_type(stub, generator, field_name, field, mask)
    ]
