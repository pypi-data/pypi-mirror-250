import enum
import inspect
import types
import typing
from datetime import datetime
from typing import Any, Dict, List, Type, get_args, get_origin
from uuid import UUID

import pydantic
import sqlalchemy
import sqlalchemy.ext.associationproxy
import sqlalchemy.orm
from inflection import underscore
from jinja2 import Environment, FileSystemLoader, select_autoescape

from lassen.db.base_class import Base as LassenBase
from lassen.db.columns import LassenUUID
from lassen.stubs.base import BaseDefinition, BaseGenerator, BaseStub, RenderedFile
from lassen.stubs.common import (
    ActiveFieldType,
    ExtractedStubImports,
    format_dict_as_kwargs,
    format_function_args,
    format_import,
    format_typehint_as_string,
    get_active_fields,
)
from lassen.stubs.definition import UniqueDefinition
from lassen.stubs.field import UNSET_VALUE
from lassen.stubs.templates import get_template_path

AUTO_CAST = (
    # These types are automatically casted by SQLAlchemy's Mapped
    # typehint merger and don't need to be repeated in the mapped_column
    sqlalchemy.Integer,
    sqlalchemy.Float,
    sqlalchemy.String,
    sqlalchemy.Boolean,
    sqlalchemy.LargeBinary,
)

DEFAULT_ORIGIN_MAPPING = {
    enum.Enum: sqlalchemy.Enum,
    list: sqlalchemy.ARRAY,
    int: sqlalchemy.Integer,
    float: sqlalchemy.Float,
    str: sqlalchemy.String,
    bytes: sqlalchemy.LargeBinary,
    bool: sqlalchemy.Boolean,
    datetime: sqlalchemy.DateTime,
    Any: sqlalchemy.JSON,
    dict: sqlalchemy.JSON,
    UUID: LassenUUID,
}


class StoreGenerator(BaseGenerator):
    origin_mapping = DEFAULT_ORIGIN_MAPPING

    def __init__(
        self, output_directory: str, custom_baseclasses: list[Type[Any]] | None = None
    ):
        super().__init__(output_directory)
        self.custom_baseclasses = custom_baseclasses or [LassenBase]

    def __call__(
        self,
        model: Type[BaseStub],
        import_hints: ExtractedStubImports,
        type_hints: dict[str, type],
    ):
        model_name = model.__name__
        fields, field_dependencies = self.get_model_fields(model, typehints=type_hints)
        table_args, table_args_dependencies = self.get_model_table_args(model)

        # Set up Jinja2 environment
        env = Environment(
            loader=FileSystemLoader(get_template_path("")),
            autoescape=select_autoescape(["html", "xml"]),
        )

        template = env.get_template("sqlalchemy.py.j2")
        # Always include the declarative base class as well as the user mixins
        model_superclasses = [
            base_class.__name__ for base_class in self.custom_baseclasses
        ]
        content = template.render(
            model_name=model_name,
            fields=fields,
            table_args=table_args,
            dependencies=sorted(
                [dependency for dependency in field_dependencies if dependency]
                + [dependency for dependency in table_args_dependencies if dependency]
                + [format_import(base_class) for base_class in self.custom_baseclasses]
            ),
            model_superclasses=", ".join(model_superclasses),
            clone_imports=[
                payload.definition for payload in import_hints.clone_imports
            ],
            clone_typechecking_imports=[
                payload.definition
                for payload in import_hints.clone_typechecking_imports
            ],
            table_name=self.model_to_tablename(model),
        )

        return RenderedFile(
            content=content,
            created_classes=[model_name],
        )

    def get_model_fields(self, model: Type[BaseStub], typehints: dict[str, type]):
        fields = get_active_fields(model, self, ActiveFieldType.PERSISTENT)
        fields_ordered = model.ordered_instance_variables()
        fields = sorted(fields, key=lambda f: fields_ordered.index(f[0]))

        declarations: list[str] = []
        dependencies: set[str | None] = set()

        instance_to_name = self.get_instance_to_name(model)

        for name, field in fields:
            typehint = typehints[name]
            mapped_typehint, dependencies1 = format_typehint_as_string(
                typehint,
                stub_resolution_directory=None,
            )
            dependencies |= set(dependencies1)

            # User-override of the default field name
            field_name = (
                name if isinstance(field.db_alias, UNSET_VALUE) else field.db_alias
            )

            # Since we want SQLAlchemy to translate the exact typehint into the column,
            # we need to check for exact class equality (versus a subclass like
            # with isinstance)
            # One specific case where this happens is Enum - it is a VARCHAR in the
            # backend, so isinstance(enum_field, sqlalchemy.String) is True. At runtime,
            # SQLAlchemy won't auto resolve this Enum to a String and needs the explicit
            # definition of the mapped_column(Enum(XX))
            if not isinstance(field.association_proxy, UNSET_VALUE):
                declaration = (
                    f"{field_name}: AssociationProxy[{mapped_typehint}] = "
                    "association_proxy"
                    f"('{field.association_proxy[0]}', '{field.association_proxy[1]}')"
                )
                dependencies |= {
                    format_import(sqlalchemy.ext.associationproxy.AssociationProxy),
                    format_import(sqlalchemy.ext.associationproxy.association_proxy),
                }
            elif field.is_relationship:
                (
                    _,
                    _,
                    dependencies2,
                ) = self.format_column_for_sqlalchemy(typehint)
                dependencies |= set(dependencies2)

                declaration = f"{field_name}: Mapped[{mapped_typehint}]"

                raw_args: list[str] = []
                extra_kwargs: dict[str, Any] = {}

                # The foreign key should point to another field on the model, which
                # during runtime corresponds to a FieldDefinition instance
                if not isinstance(field.foreign_key, UNSET_VALUE):
                    foreign_key_name = instance_to_name.get(id(field.foreign_key))
                    if not foreign_key_name:
                        raise ValueError(
                            f"Unable to find {field.foreign_key} in model"
                            f" {model.__name__}"
                        )
                    raw_args.append(f"foreign_keys=[{foreign_key_name}]")

                    # If the foreign key is self-referential, we should make sure that
                    # we clarify the direction of the relationship. When attributes are
                    # set, they should _always_ be set in the database to the object
                    # they are set on in the `create` constructor. Otherwise we can
                    # see a backref being inferred automatically and the relationship
                    # value being put on the wrong object. Without specifying the
                    # remote_side here, we can sometimes see A.relationship = B
                    # resulting in B.relationship = A.
                    if field.foreign_key.foreign_key:
                        table, _ = field.foreign_key.foreign_key.split(".")
                        if table == self.model_to_tablename(model):
                            raw_args.append("remote_side=[_id]")

                if not isinstance(field.backref, UNSET_VALUE):
                    extra_kwargs["backref"] = field.backref
                if not isinstance(field.back_populates, UNSET_VALUE):
                    extra_kwargs["back_populates"] = field.back_populates

                declaration += (
                    f" = relationship({format_function_args(raw_args, extra_kwargs)})"
                )
                dependencies.add(format_import(sqlalchemy.orm.relationship))
            else:
                (
                    column_typehint,
                    column_class,
                    dependencies2,
                ) = self.format_column_for_sqlalchemy(typehint)
                dependencies |= set(dependencies2)

                declaration = f"{field_name}: Mapped[{mapped_typehint}]"

                args = []
                keyword_args = {}

                # Use the original name in the database itself
                if not isinstance(field.db_alias, UNSET_VALUE):
                    args.append(f"'{name}'")

                if column_typehint and column_class.__class__ not in AUTO_CAST:
                    args.append(column_typehint)

                if not isinstance(field.primary_key, UNSET_VALUE):
                    keyword_args["primary_key"] = True
                if not isinstance(field.default, UNSET_VALUE):
                    keyword_args["default"] = field.default
                if not isinstance(field.foreign_key, UNSET_VALUE):
                    args.append(f"ForeignKey('{field.foreign_key}')")
                    dependencies.add(format_import(sqlalchemy.ForeignKey))
                if field.index:
                    keyword_args["index"] = True

                formatted_args = [
                    *args,
                    *([format_dict_as_kwargs(keyword_args)] if keyword_args else []),
                ]
                if formatted_args:
                    declaration += f" = mapped_column({', '.join(formatted_args)})"

            declarations.append(declaration)

        if not declarations:
            declarations.append("pass")

        return declarations, list(dependencies)

    def get_model_table_args(self, model: Type[BaseStub]):
        definitions: list[tuple[str, BaseDefinition]] = list(
            inspect.getmembers(model, lambda m: isinstance(m, BaseDefinition))
        )

        definitions_ordered = model.ordered_instance_variables()
        definitions = sorted(definitions, key=lambda f: definitions_ordered.index(f[0]))

        instance_to_name = self.get_instance_to_name(model)

        declarations: list[str] = []
        dependencies: set[str] = set()

        for _, definition in definitions:
            if isinstance(definition, UniqueDefinition):
                field_names = [
                    f"'{instance_to_name[id(field)]}'" for field in definition.fields
                ]

                declarations.append(
                    f"UniqueConstraint({', '.join(field_names)},"
                    f" name='{definition.name}')"
                )
                dependencies.add(
                    format_import(sqlalchemy.UniqueConstraint),
                )

        return declarations, list(dependencies)

    def get_instance_to_name(self, model: Type[BaseStub]) -> dict[int, str]:
        """
        Allows us to recover the variable name when function arguments
        are passed in explicitly as set-variables.
        """
        instance_variable: list[tuple[str, Any]] = list(inspect.getmembers(model))

        return {id(field): name for name, field in instance_variable}

    def format_column_for_sqlalchemy(
        self, typehint: Any
    ) -> tuple[str, Any, list[str | None]]:
        if inspect.isclass(typehint) and issubclass(typehint, enum.Enum):
            enum_handler = self.origin_mapping[enum.Enum]
            return (
                f"{enum_handler.__name__}({typehint.__name__})",
                enum_handler(typehint),
                [format_import(enum_handler)],
            )
        elif inspect.isclass(typehint) and issubclass(typehint, BaseStub):
            return (
                typehint.__name__,
                typehint,
                # Don't import other class dependencies for now
                # TODO: Add typehinting only support here for their new file paths
                [],
            )
        elif typehint in [int, float, str, bool, datetime, bytes, Any]:
            raw_class = self.origin_mapping[typehint]
            return (f"{raw_class.__name__}()", raw_class(), [format_import(raw_class)])
        elif typehint == UUID:
            raw_class = self.origin_mapping[typehint]
            return (
                f"{raw_class.__name__}(as_uuid=True)",
                raw_class(as_uuid=True),
                [format_import(raw_class)],
            )
        elif isinstance(typehint, str):
            # Forward reference, assume this is to another class
            return (f"'{typehint}'", typehint, [])
        elif (
            inspect.isclass(typehint)
            and issubclass(typehint, pydantic.BaseModel)
            and not issubclass(typehint, BaseStub)
        ):
            raw_class = self.origin_mapping[Any]
            return (f"{raw_class.__name__}()", raw_class(), [format_import(raw_class)])
        elif typehint in self.origin_mapping and typehint not in DEFAULT_ORIGIN_MAPPING:
            # User defined typehint for another, unsupported class
            raw_class = self.origin_mapping[typehint]
            return (f"{raw_class.__name__}()", raw_class(), [format_import(raw_class)])
        else:
            origin = get_origin(typehint)
            args = get_args(typehint)
            if origin is list or origin is List:
                # Verify a homogeneous list
                unique_args = set(args)
                if len(unique_args) > 1:
                    raise ValueError("Lists with multiple types are not supported")
                if (
                    args
                    and inspect.isclass(args[0])
                    and issubclass(args[0], pydantic.BaseModel)
                ):
                    # If the sub-model is a pydantic value we should format as a regular
                    # json blob
                    return self.format_column_for_sqlalchemy(Any)
                elif args and isinstance(args[0], (type, str)):
                    list_handler = self.origin_mapping[list]
                    (
                        cast_arg,
                        cast_class_arg,
                        dependencies,
                    ) = self.format_column_for_sqlalchemy(args[0])

                    return (
                        f"{list_handler.__name__}({cast_arg})",
                        list_handler(cast_class_arg),
                        [format_import(list_handler), *dependencies],
                    )
            elif origin is dict or origin is Dict:
                raw_class = self.origin_mapping[dict]
                return (
                    f"{raw_class.__name__}()",
                    raw_class(),
                    [format_import(raw_class)],
                )
            elif origin is typing.Union or origin == types.UnionType:  # noqa E721
                # Assumes that all Union types are nullable
                nullable_args = [arg for arg in args if arg is not type(None)]
                if len(nullable_args) > 1:
                    raise ValueError(
                        "Unions with multiple non-None types are not supported"
                    )
                (
                    non_null_arg,
                    cast_class_arg,
                    dependencies,
                ) = self.format_column_for_sqlalchemy(nullable_args[0])
                return (non_null_arg, cast_class_arg, dependencies)

        raise NotImplementedError(f"Type hint {typehint} not supported")

    def model_to_tablename(self, model: Type[BaseStub]) -> str:
        return underscore(model.__name__)
