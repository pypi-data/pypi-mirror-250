from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    Type,
    TypeVar,
    overload,
)

from pydantic import BaseModel
from sqlalchemy import Column, Table
from sqlalchemy.orm import Query, Session
from sqlalchemy.orm.attributes import InstrumentedAttribute

from lassen.enums import FilterTypeEnum
from lassen.queries import chain_select
from lassen.store.base import ModelType, StoreCommonBase

FilterSchemaType = TypeVar("FilterSchemaType", bound=BaseModel)


@dataclass
class ParsedColumnFilters:
    explicit_columns: list[Column | InstrumentedAttribute]
    implicit_columns: list[Column | InstrumentedAttribute]
    joins: list[Any]


class StoreFilterMixin(
    StoreCommonBase[ModelType], Generic[ModelType, FilterSchemaType]
):
    """
    A mixin to add simple exact-match filtering to a store.

    """

    archived_column_name = "archived"

    def __init__(self, model: Type[ModelType]):
        super().__init__(model)

    @overload
    def get_multi(
        self,
        db: Session,
        filter: FilterSchemaType,
        *,
        skip: int | None = 0,
        limit: int | None = None,
        include_archived: bool = False,
        only_fetch_columns: None = None,
    ) -> list[ModelType]:
        ...

    @overload
    def get_multi(
        self,
        db: Session,
        filter: FilterSchemaType,
        *,
        only_fetch_columns: list[Column | InstrumentedAttribute | chain_select],
        skip: int | None = 0,
        limit: int | None = None,
        include_archived: bool = False,
    ) -> list[tuple[Any, ...]]:
        ...

    def get_multi(
        self,
        db: Session,
        filter: FilterSchemaType,
        skip: int | None = 0,
        limit: int | None = None,
        include_archived: bool = False,
        only_fetch_columns: list[Column | InstrumentedAttribute | chain_select]
        | None = None,
    ) -> list[ModelType] | list[tuple[Any, ...]]:
        # We should make sure the current session is flushed before trying to
        # query on it. This works around the fact that SQLAlchemy uses a
        # separate database transaction for read operations than it does
        # for write operations. This won't actually commit the transaction.
        db.flush()

        query: Query

        parsed_fetch_columns: ParsedColumnFilters | None = None
        if only_fetch_columns:
            query, parsed_fetch_columns = self.build_column_fetch(
                db=db, only_fetch_columns=only_fetch_columns
            )
        else:
            query = db.query(self.model)

        query = self.build_filter(query, filter, include_archived)
        query = self._order_by(query)

        if skip is not None:
            query = query.offset(skip)
        if limit is not None:
            query = query.limit(limit)

        results = query.all()

        if parsed_fetch_columns:
            return self.postprocess_column_fetch(
                results=results, parsed_columns=parsed_fetch_columns
            )

        return results

    def count_multi(
        self,
        db: Session,
        filter: FilterSchemaType,
        include_archived: bool = False,
    ):
        query = db.query(self.model)
        query = self.build_filter(query, filter, include_archived)
        return query.count()

    def build_filter(
        self, query: Query, filter: FilterSchemaType, include_archived: bool
    ):
        model_table: Table = getattr(self.model, "__table__")
        model_columns = model_table.columns

        for field, value in filter.model_dump(exclude_unset=True).items():
            # Split our special suffixes, if present
            parsed_field = field.split("__")
            raw_field = parsed_field[0]
            logic_type = (
                FilterTypeEnum(parsed_field[1])
                if len(parsed_field) > 1
                else FilterTypeEnum.EQUAL
            )

            model_value = self.attribute_from_key(raw_field)
            if logic_type == FilterTypeEnum.EQUAL:
                query = query.filter(model_value == value)
            elif logic_type == FilterTypeEnum.NOT:
                query = query.filter(model_value != value)
            elif logic_type == FilterTypeEnum.IN:
                query = query.filter(model_value.in_(value))
            elif logic_type == FilterTypeEnum.NOT_IN:
                query = query.filter(~model_value.in_(value))
            elif logic_type == FilterTypeEnum.LESS_THAN:
                query = query.filter(model_value < value)
            elif logic_type == FilterTypeEnum.LESS_THAN_OR_EQUAL:
                query = query.filter(model_value <= value)
            elif logic_type == FilterTypeEnum.GREATER_THAN:
                query = query.filter(model_value > value)
            elif logic_type == FilterTypeEnum.GREATER_THAN_OR_EQUAL:
                query = query.filter(model_value >= value)
            else:
                raise ValueError(
                    f"Key special suffix `{logic_type}` in `{field}` is not supported"
                )

        # Only allow include_archived behavior if the model has an archived column
        model_column_names = [column.name for column in model_columns]
        if self.archived_column_name in model_column_names:
            if include_archived:
                query = query.execution_options(include_archived=True)

        return query

    def build_column_fetch(
        self,
        db: Session,
        only_fetch_columns: list[Column | InstrumentedAttribute | chain_select],
    ):
        fetch_explicit_columns: list[Column | InstrumentedAttribute] = []
        fetch_implicit_columns: list[Column | InstrumentedAttribute] = []
        fetch_joins: list[Any] = []

        for fetch_filter in only_fetch_columns:
            if isinstance(fetch_filter, (Column, InstrumentedAttribute)):
                fetch_explicit_columns.append(fetch_filter)
            elif isinstance(fetch_filter, chain_select):
                fetch_explicit_columns += fetch_filter.explicit_query_elements
                fetch_implicit_columns += fetch_filter.implicit_query_elements
                fetch_joins += fetch_filter.joins
            else:
                raise ValueError(f"Invalid fetch filter type: {type(fetch_filter)}")

        query = db.query(*fetch_explicit_columns, *fetch_implicit_columns)
        if fetch_joins:
            for join in fetch_joins:
                query = query.join(*join)

        return query, ParsedColumnFilters(
            explicit_columns=fetch_explicit_columns,
            implicit_columns=fetch_implicit_columns,
            joins=fetch_joins,
        )

    def postprocess_column_fetch(
        self,
        results: list[tuple[Any, ...]],
        parsed_columns: ParsedColumnFilters,
    ):
        """
        Only return the columns that were explicitly requested by the user.
        """
        # By convention, we assume that explicit columns are returned first
        # followed by implicit columns
        return [result[: len(parsed_columns.explicit_columns)] for result in results]

    def _order_by(self, query: Query):
        # By default, no-op
        return query
