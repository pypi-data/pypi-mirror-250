import builtins
import enum
import inspect
import types
import typing
from pathlib import Path
from typing import (
    Any,
    Type,
    TypeVar,
    get_args,
    get_origin,
    get_type_hints,
)

import pydantic

from lassen.constants import CLIENT_STUB_DIRECTORY
from lassen.io import guess_package_location
from lassen.stubs.base import BaseStub
from lassen.stubs.common.stub_imports import ExtractedStubImports, SubImportDefinition

T = TypeVar("T")


def format_import(cls):
    # Get module of the class
    module = inspect.getmodule(cls)

    if isinstance(cls, typing.ForwardRef):
        return None

    if module is None or module.__name__ == "__main__":
        raise ValueError(f"{cls} is not part of a module.")

    module_name = module.__name__
    class_name = cls.__name__
    if module == builtins:
        return None
    return f"from {module_name} import {class_name}"


def get_resolved_type_hints(
    model: Type[Any], stub_models: list[Type[Any]], stub_imports: ExtractedStubImports
) -> dict[str, Type[Any]]:
    """
    Get type hints from a model, resolving forward references
    with priority to the files that contain actual references.

    :param model: the model class for which to resolve type hints
    :param stub_models: list of all model classes to use for resolving
        forward references
    :param stub_imports: ExtractedStubImports object containing imports
        from the stub files

    """
    # Initialize an empty local namespace
    localns = {}

    # Process type-checking imports first, as they have priority
    for import_def in stub_imports.clone_typechecking_imports:
        for sub_import in import_def.module_definitions:
            for other_model in stub_models:
                if match_import_with_model(other_model, sub_import):
                    localns[other_model.__name__] = other_model

    # Process normal imports, but only if they don't overwrite existing entries
    # in localns
    for import_def in stub_imports.clone_imports:
        for sub_import in import_def.module_definitions:
            for other_model in stub_models:
                name = other_model.__name__
                if name not in localns and match_import_with_model(
                    other_model, sub_import
                ):
                    localns[name] = other_model

    # Now get and return the type hints, resolving forward references using localns
    return get_type_hints(model, localns=localns)


def match_import_with_model(model: Type[Any], sub_import: SubImportDefinition) -> bool:
    model_module = model.__module__
    model_name = model.__name__

    if (
        sub_import.module_name
        and model_module.endswith(sub_import.module_name)
        and sub_import.object_name == model_name
    ):
        return True

    if sub_import.module_path:
        model_path = Path(inspect.getfile(model))
        if (
            model_path == sub_import.module_path
            and sub_import.object_name == model_name
        ):
            return True

    return False


def format_typehint_as_string(
    typehint,
    stub_resolution_directory: str | None = None,
) -> tuple[str, list[str]]:
    """
    Prepare a generic typehint for string insertion into a template as a hint value

    Effectively just takes the runtime value of a typehint and converts it back into the
    code that creates that typehint

    :param stub_resolution_directory: If provided, will format the typehint of BaseStubs
    into the provided directory. This is helpful if generators want to link a stub
    reference to an actual materialized view on the filesystem.

    """
    origin = get_origin(typehint)
    args = get_args(typehint)

    # Handle case for NoneType
    if typehint is type(None):
        return "None", []

    # Handle case for Unions, which might represent nullable fields
    if origin is typing.Union or origin == types.UnionType:  # noqa E721
        child_typehints = [
            format_typehint_as_string(
                t, stub_resolution_directory=stub_resolution_directory
            )
            for t in args
        ]
        union_args = ", ".join([child_name for child_name, _ in child_typehints])
        return f"Union[{union_args}]", [
            child_dep for _, child_deps in child_typehints for child_dep in child_deps
        ] + [format_import(typing.Union)]

    # Handle case for Enum
    if isinstance(typehint, enum.EnumMeta):
        return typehint.__name__, [format_import(typehint)]

    # Handle case for built-in types
    if origin is None and not args:
        if (
            inspect.isclass(typehint)
            and issubclass(typehint, pydantic.BaseModel)
            and not issubclass(typehint, BaseStub)
        ):
            # Support non-stub pydantic schemas
            return f"{typehint.__name__}", [format_import(typehint)]
        elif inspect.isclass(typehint) and issubclass(typehint, BaseStub):
            if stub_resolution_directory:
                root_project_path = guess_package_location(CLIENT_STUB_DIRECTORY)
                project_name = root_project_path.name
                stub_resolution_components = ".".join(
                    [
                        component
                        for component in stub_resolution_directory.split("/")
                        if component.strip()
                    ]
                )
                # Rename the model import so we don't conflict with other imports
                model_reference = f"{typehint.__name__}Model"
                return model_reference, [
                    f"from {project_name}.{stub_resolution_components }."
                    f"{typehint.get_filename()} import {typehint.__name__} "
                    f"as {model_reference}"
                ]
            else:
                # Keep as a forward reference
                return f"'{typehint.__name__}'", []
        else:
            return typehint.__name__, [format_import(typehint)]

    # Handle case for generic types like List, Dict
    if origin is not None or args:
        if origin:
            typehint_name = origin.__name__
        else:
            typehint_name = typehint.__name__

        arg_names: list[str] = []
        arg_deps: list[str] = []

        for arg in args:
            arg_name, arg_dep = format_typehint_as_string(
                arg, stub_resolution_directory=stub_resolution_directory
            )
            arg_names.append(arg_name)
            arg_deps.extend(arg_dep)

        arg_types = ", ".join(arg_names)
        return f"{typehint_name}[{arg_types}]", arg_deps

    raise NotImplementedError(f"Type hint {typehint} not supported")


def resolve_core_types(typehint):
    """
    Takes a typehint, potentially one with multiple options, and returns the objects
    that are the core types that are being referenced.

    """

    origin = get_origin(typehint)
    args = get_args(typehint)

    # We've exhausted the typehint
    if not origin:
        if typehint is None:
            return []
        return [typehint]

    return [resolved_type for arg in args for resolved_type in resolve_core_types(arg)]
