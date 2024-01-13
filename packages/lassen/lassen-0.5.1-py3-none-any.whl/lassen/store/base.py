import types
from functools import lru_cache
from inspect import isclass
from typing import (
    Any,
    AsyncIterable,
    Generic,
    Iterable,
    Type,
    TypeVar,
    get_args,
    get_type_hints,
)
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import inspect
from sqlalchemy.orm import Session, class_mapper
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.properties import ColumnProperty

from lassen.db.base_class import Base
from lassen.io import get_batch, get_batch_async

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


@lru_cache(maxsize=None)
def get_instance_primary_key(model: Type[ModelType]):
    mapper = class_mapper(model)
    for prop in mapper.iterate_properties:
        if isinstance(prop, ColumnProperty):
            column_attr = getattr(model, prop.key)
            if (
                hasattr(column_attr, "expression")
                and column_attr.expression.key == mapper.primary_key[0].name
            ):
                return prop.key
    raise ValueError(f"Model `{model}` has no primary key")


class StoreCommonBase(Generic[ModelType]):
    model: Type[ModelType]

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def attribute_from_key(self, column_name: str) -> InstrumentedAttribute[Any]:
        """
        SQLAlchemy supports name aliases, where the instance name is different
        from the actual column name. Given a column name, this function returns the
        instance type that's attached to the model.

        """
        for attr, column in self.model.__mapper__.columns.items():
            if column.name == column_name:
                return getattr(self.model, attr)
        raise ValueError(f"Column `{column_name}` not found in model `{self.model}`")


class StoreBase(
    StoreCommonBase[ModelType], Generic[ModelType, CreateSchemaType, UpdateSchemaType]
):
    """
    A Store is used to interact with the database. It provides the bridge from
    pydantic models (that declaratively define the allowable creations, updates, etc.)
    to the underlying SQLAlchemy models that are used to interact with the database.

    It supports per-object operations such as:
    - Create operations
    - Update operations
    - Delete operations

    In addition, it supports bulk operations. These bulk operations write
    directly to the database, so they gain throughput at the expense of
    features of the ORM like updating objects in-memory. They are still
    part of the overall transaction block so they are rolled back if
    there is an exception later in the handling.

    """

    relationship_attributes: dict[str, Type[Base]]

    def __init__(self, model: Type[ModelType]):
        super().__init__(model)

        # Mapping of relationships to their SQLAlchemy models
        self.relationship_attributes = {
            key: relationship.mapper.class_
            for key, relationship in model.__mapper__.relationships.items()
        }

    def get(self, db: Session, id: Any) -> ModelType | None:
        db.flush()
        return (
            db.query(self.model).filter(self.attribute_from_key("id") == id).first()
        )  # type: ignore

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        # obj_in_data = jsonable_encoder(obj_in)
        obj_in_data = obj_in.model_dump(exclude_unset=True)
        obj_in_data = self.create_dependencies(db, obj_in_data, obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        model_columns = self.model.__table__.columns

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        update_data = self.create_dependencies(db, update_data, obj_in)
        for field, value in update_data.items():
            if field not in model_columns and field not in self.relationship_attributes:
                raise ValueError(f"Model `{self.model}` has no column `{field}`")
            setattr(db_obj, field, value)
        db.add(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int | UUID) -> ModelType | None:
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
        return obj

    def create_dependencies(
        self, db: Session, obj_in_data: dict[str, Any], obj_in: Any
    ):
        """
        Creates nested objects that are contained within the primary.
        Note that this function only creates one-depth of dependencies.
        If you have a dependency that has a dependency,
        you will need to create that dependency separately.

        """
        # Iterate over the dependent relationships and attempt to create these first
        for relationship, relationship_class in self.relationship_attributes.items():
            if relationship not in obj_in_data:
                continue

            static_value = obj_in_data[relationship]
            static_value_original = (
                obj_in[relationship]
                if isinstance(obj_in, dict)
                else getattr(obj_in, relationship)
            )
            database_value: list[Base] | Base | None = None

            # Determine if we should create a list
            # Otherwise assume this is an object
            if isinstance(static_value, list):
                database_value = []
                for value, original_value in zip(static_value, static_value_original):
                    # If this is a dict, we should cast it otherwise
                    # assume it's a SQLAlchemy object
                    if isinstance(original_value, Base):
                        database_value.append(value)
                    else:
                        database_object = relationship_class(**value)
                        db.add(database_object)
                        # db.commit()
                        # db.refresh(database_object)
                        database_value.append(database_object)

                obj_in_data[relationship] = database_value
            else:
                # If this is a dict, we should cast it otherwise
                # assume it's a SQLAlchemy object
                if isinstance(static_value, dict):
                    # Create the relationship object
                    database_value = relationship_class(**static_value)
                    db.add(database_value)
                    # db.commit()
                    # db.refresh(database_value)
                else:
                    database_value = static_value

            # Update the relationship with the newly created object
            obj_in_data[relationship] = database_value

        return obj_in_data

    def validate_types(self):
        # Get the runtime value of the schemas attached to this class
        base_class_args = [
            base_class
            for base_class in getattr(self.__class__, "__orig_bases__")
            if base_class.__origin__ == StoreBase
        ]
        if not base_class_args:
            raise ValueError("StoreBase must be subclassed with type arguments")

        _, create_schema, update_schema = get_args(base_class_args[0])

        def validate_arg_model_order(args):
            """
            Ensure that models are declared before their SQLAlchemy
            counterparts. Otherwise objects will be cast as schemas
            where we typically want them to remain as SQLAlchemy objects.
            """
            index_of_model = [
                i for i, x in enumerate(args) if isclass(x) and issubclass(x, Base)
            ]
            if index_of_model:
                if min(index_of_model) > 0:
                    raise ValueError(
                        "SQLAlchemy Model must come first in a list of"
                        " typehints, actual order: {args}"
                    )

            # Recursively do this for all union types
            for arg in args:
                if isinstance(arg, types.UnionType):
                    validate_arg_model_order(arg.__args__)

        # Get all the nested elements that involve models and
        for schema in [create_schema, update_schema]:
            # Iterate over all typehints for the class
            schema_typehints = get_type_hints(schema)

            for typehint in schema_typehints.values():
                if hasattr(typehint, "__args__"):
                    validate_arg_model_order(typehint.__args__)

    def bulk_create(
        self,
        db: Session,
        schemas: Iterable[CreateSchemaType],
        batch_size: int = 100,
    ):
        """
        Bulk inserts the given create schemas.

        Note that this won't take care of inserting dependencies, unlike
        the standard `create` function.

        """
        # This approach is faster, by about 1/3rd if we don't have
        # to return the primary keys
        for batch in get_batch(schemas, batch_size):
            resolved_relationships = self.build_bulk_objects(batch)

            db.bulk_insert_mappings(
                self.model.__mapper__,
                resolved_relationships,
            )

    async def bulk_create_async(
        self,
        db: Session,
        schemas: AsyncIterable[CreateSchemaType],
        batch_size: int = 100,
    ):
        """
        Bulk inserts the given create schemas.

        Note that this won't take care of inserting dependencies, unlike
        the standard `create` function.

        """
        # This approach is faster, by about 1/3rd if we don't have
        # to return the primary keys
        async for batch in get_batch_async(schemas, batch_size):
            resolved_relationships = self.build_bulk_objects(batch)

            db.bulk_insert_mappings(
                self.model.__mapper__,
                resolved_relationships,
            )

    def bulk_update(
        self,
        db: Session,
        update_elements: Iterable[tuple[int | UUID, UpdateSchemaType]],
        batch_size: int = 100,
    ):
        """
        :param update_elements: Payloads formatted as (id to update, update payloads)

        """
        primary_key_name = primary_key_name = get_instance_primary_key(self.model)

        for batch in get_batch(update_elements, batch_size):
            resolved_relationships = self.build_bulk_objects(
                [obj_in for _, obj_in in batch]
            )

            db.bulk_update_mappings(
                self.model.__mapper__,
                [
                    {**obj_in, primary_key_name: obj_id}
                    for (obj_id, _), obj_in in zip(batch, resolved_relationships)
                ],
            )

        # Expires already-loaded objects so that they are reloaded
        # with the new updated values
        # This shouldn't affect objects queued for modification in the
        # current transaction
        db.expire_all()

    async def bulk_update_async(
        self,
        db: Session,
        update_elements: AsyncIterable[tuple[int | UUID, UpdateSchemaType]],
        batch_size: int = 100,
    ):
        """
        :param update_elements: Payloads formatted as (id to update, update payloads)

        """
        primary_key_name = get_instance_primary_key(self.model)

        async for batch in get_batch_async(update_elements, batch_size):
            resolved_relationships = self.build_bulk_objects(
                [obj_in for _, obj_in in batch]
            )

            db.bulk_update_mappings(
                self.model.__mapper__,
                [
                    {**obj_in, primary_key_name: obj_id}
                    for (obj_id, _), obj_in in zip(batch, resolved_relationships)
                ],
            )
        db.expire_all()

    def build_bulk_objects(
        self, batch_schemas: Iterable[CreateSchemaType] | Iterable[UpdateSchemaType]
    ):
        """
        Unlike the regular ORM, batch insertions don't automatically resolve the
        relationships that are defined on each object. model.__mapper__ actually
        excludes relationships for this reason and only defines the raw DB columns.
        This function sniffs for the relationship IDs and inserts these instead of
        the raw objects.

        """
        inspector = inspect(self.model)
        relationship_to_foreign_key_map: dict[str, str] = {}

        for relationship in inspector.relationships:
            # Get the key to access the related object in the schema and the foreign
            # key attribute
            if not relationship.local_remote_pairs:
                continue
            for local_column, _ in relationship.local_remote_pairs:
                if not local_column.key:
                    continue
                relationship_to_foreign_key_map[relationship.key] = local_column.key

        # Prepare main object data with resolved foreign keys
        main_objects_data: list[dict[str, Any]] = []
        for schema in batch_schemas:
            main_object_data = schema.model_dump(exclude_unset=True)

            # Resolve foreign keys from related object IDs
            for (
                relationship_key,
                foreign_key_name,
            ) in relationship_to_foreign_key_map.items():
                related_object = getattr(schema, relationship_key, None)
                if related_object:
                    main_object_data[foreign_key_name] = getattr(
                        related_object,
                        get_instance_primary_key(related_object.__class__),
                    )

            main_objects_data.append(main_object_data)

        return main_objects_data
