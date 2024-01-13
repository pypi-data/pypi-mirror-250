import inspect
import types
import typing
from typing import Any, Type, get_args, get_origin

from jinja2 import Environment, FileSystemLoader, select_autoescape

from lassen.enums import FilterTypeEnum
from lassen.stubs.base import BaseGenerator, BaseStub, RenderedFile
from lassen.stubs.common import (
    ActiveFieldType,
    ExtractedStubImports,
    format_dict_as_kwargs,
    format_typehint_as_string,
    get_active_fields,
    resolve_core_types,
)
from lassen.stubs.field import UNSET_VALUE
from lassen.stubs.templates import get_template_path


def is_optional(type_hint):
    origin = get_origin(type_hint)
    args = get_args(type_hint)

    if origin is typing.Union or origin == types.UnionType:  # noqa E721
        return any(arg is type(None) for arg in args)
    elif isinstance(type_hint, type):
        return type_hint is type(None)
    return False


def make_optional(type_hint):
    if is_optional(type_hint):
        # The type hint is already Optional
        return type_hint
    else:
        origin = get_origin(type_hint)
        args = get_args(type_hint)

        if origin is typing.Union or origin == types.UnionType:  # noqa E721
            # Convert the Union to Optional by adding None as an argument
            return typing.Union[*args, type(None)]
        else:
            # If the type hint is not a Union, make it Optional
            return typing.Optional[type_hint]


class SchemaGenerator(BaseGenerator):
    def __init__(
        self,
        output_directory: str,
        use_sqlalchemy_relationships: bool = True,
    ):
        """
        :param use_sqlalchemy_relationships: Use sqlalchemy relationships for object
            creation and deltion. This plays well with transaction-based workflows where
            objects are queued up locally before being committed.

        """
        super().__init__(output_directory)
        self.use_sqlalchemy_relationships = use_sqlalchemy_relationships

    def __call__(
        self,
        model: Type[BaseStub],
        import_hints: ExtractedStubImports,
        type_hints: dict[str, type],
    ):
        model_name = model.__name__

        # We use the same base schema but make some configuration choices based on
        # the majority of situations where these tend to be used:
        # 1. Updates are PATCH-like requests so we should allow None values across
        #   the board
        # 2. Read requests should be reading from an underlying data object, and
        #   therefore shouldn't have any default values
        create_fields, create_deps = self.get_model_fields(
            model,
            field_predicate=ActiveFieldType.CREATE,
            typehints=type_hints,
            stubs_to_models=self.use_sqlalchemy_relationships,
        )
        update_fields, update_deps = self.get_model_fields(
            model,
            field_predicate=ActiveFieldType.UPDATE,
            force_optional=True,
            typehints=type_hints,
            stubs_to_models=self.use_sqlalchemy_relationships,
        )
        read_fields, read_deps = self.get_model_fields(
            model,
            field_predicate=ActiveFieldType.READ,
            include_defaults=False,
            typehints=type_hints,
        )
        filter_fields, filter_deps = self.get_model_fields(
            model,
            field_predicate=ActiveFieldType.FILTER,
            force_optional=True,
            typehints=type_hints,
        )
        augmented_filters, augmented_deps = self.get_augmented_filter_fields(
            model, typehints=type_hints
        )

        all_dependencies = set(
            create_deps + update_deps + read_deps + filter_deps + augmented_deps
        )

        # Set up Jinja2 environment
        env = Environment(
            loader=FileSystemLoader(get_template_path("")),
            autoescape=select_autoescape(["html", "xml"]),
        )

        template = env.get_template("schema.py.j2")
        content = template.render(
            model_name=model_name,
            create_fields=create_fields,
            update_fields=update_fields,
            read_fields=read_fields,
            filter_fields=filter_fields + augmented_filters,
            dependencies=sorted(
                [dependency for dependency in all_dependencies if dependency]
            ),
            clone_imports=[
                payload.definition for payload in import_hints.clone_imports
            ],
            clone_typechecking_imports=[
                payload.definition
                for payload in import_hints.clone_typechecking_imports
            ],
        )

        return RenderedFile(
            content=content,
            created_classes=[
                model_name,
                f"{model_name}Create",
                f"{model_name}Update",
                f"{model_name}Filter",
                f"{model_name}Base",
            ],
        )

    def get_model_fields(
        self,
        model: Type[BaseStub],
        *,
        typehints: dict[str, type],
        field_predicate: ActiveFieldType | None = None,
        force_optional: bool = False,
        include_defaults: bool = True,
        stubs_to_models: bool = False,
    ):
        """
        :param stubs_to_models: Whether to resolve stub references to sqlalchemy
        models (useful for creations and deletions) or to the pydantic schemas
        themselves (useful for output resolution).

        """
        fields = get_active_fields(model, self, field_predicate)
        fields_ordered = model.ordered_instance_variables()
        fields = sorted(fields, key=lambda f: fields_ordered.index(f[0]))

        declarations: list[str] = []
        dependencies: set[str | None] = set()

        for name, field in fields:
            typehint = typehints[name]
            if force_optional:
                typehint = make_optional(typehint)

            stub_resolution_directory: str | None = None

            # If we want to link stub definitions to a model, we need a store
            # generator on the target model
            if stubs_to_models:
                to_stubs = [
                    typehint_partial
                    for typehint_partial in resolve_core_types(typehint)
                    if inspect.isclass(typehint_partial)
                    and issubclass(typehint_partial, BaseStub)
                ]
                if len(to_stubs) > 1:
                    raise ValueError(
                        f"Field {model.__name__}.{name} is typehinted to multiple "
                        f"stubs: {to_stubs}. Please only typehint to a single stub."
                    )
                if len(to_stubs) == 1:
                    core_typehint = to_stubs[0]
                    store_generator = self.get_model_store(core_typehint)
                    if store_generator is False:
                        raise ValueError(
                            f"Field {model.__name__}.{name} is typehinted to "
                            f"{core_typehint.__name__} ({core_typehint}) but this "
                            "stub does not have a store generator. Please add a store "
                            f"generator to the {core_typehint.__name__} stub."
                        )

                    # Stub definitions should resolve to the models themselves, to allow
                    # uses to CreateSchema(relationship=Model) directly.
                    stub_resolution_directory = store_generator.output_directory

            mapped_typehint, type_dependencies = format_typehint_as_string(
                typehint,
                stub_resolution_directory=stub_resolution_directory,
            )

            declaration = f"{name}: {mapped_typehint}"
            field_arguments: dict[str, Any] = {}
            if include_defaults:
                if force_optional:
                    field_arguments["default"] = None
                elif not isinstance(field.default, UNSET_VALUE):
                    if callable(field.default):
                        field_arguments["default_factory"] = field.default
                    else:
                        field_arguments["default"] = field.default
                elif is_optional(typehint):
                    # Default typehint is optional, so we should set the default to None
                    # so users don't have to manually set it
                    field_arguments["default"] = None

            if field.description:
                field_arguments["description"] = field.description

            if field.examples:
                field_arguments["examples"] = field.examples

            if field_arguments:
                declaration += f" = Field({format_dict_as_kwargs(field_arguments)})"
            declarations.append(declaration)
            dependencies |= set(type_dependencies)

        if not declarations:
            declarations.append("pass")

        return declarations, list(dependencies)

    def get_model_store(self, model: Type[BaseStub]):
        """
        If a field is typehinted to another stub, we want to allow users to input
        the sqlalchemy model itself.

        class Child(BaseStub):
            parent: Parent

        If so, we should ensure that `Parent` has a store generator to make sure this
        model will actually be generated.

        """
        from lassen.stubs.generators.store import StoreGenerator

        for generator in model.get_generators():
            if isinstance(generator, StoreGenerator):
                return generator
        return False

    def get_augmented_filter_fields(
        self,
        model: Type[BaseStub],
        typehints: dict[str, type],
    ):
        """
        Format field filters, like `id__in` or `value__not`

        These have a different syntax pattern than our other fields, which are
        1:1 to the declaration name.

        """
        fields = get_active_fields(model, self, ActiveFieldType.FILTER)
        fields_ordered = model.ordered_instance_variables()
        filter_fields = sorted(fields, key=lambda f: fields_ordered.index(f[0]))

        declarations: list[str] = []
        dependencies: set[str | None] = set()

        for name, field in filter_fields:
            if isinstance(field.filter_extensions, UNSET_VALUE):
                continue

            typehint = typehints[name]

            for filter_extension in field.filter_extensions:
                if filter_extension == FilterTypeEnum.IN:
                    typehint = make_optional(typing.List[typehint])  # type: ignore
                elif filter_extension == FilterTypeEnum.NOT_IN:
                    typehint = make_optional(typing.List[typehint])  # type: ignore
                else:
                    typehint = make_optional(typehint)

                mapped_typehint, type_dependencies = format_typehint_as_string(typehint)

                declaration = f"{name}__{filter_extension.value}: {mapped_typehint}"
                field_arguments: dict[str, Any] = {
                    "default": None,
                }
                if field.description:
                    field_arguments["description"] = field.description

                if field_arguments:
                    declaration += f" = Field({format_dict_as_kwargs(field_arguments)})"

                declarations.append(declaration)
                dependencies |= set(type_dependencies)

        return declarations, list(dependencies)
