from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Query

from lassen.db.session import get_db_context
from lassen.enums import FilterTypeEnum
from lassen.queries import chain_select
from lassen.store import StoreBase, StoreFilterMixin
from lassen.tests.model_fixtures import (
    SampleChainedChild,
    SampleChainedChildCreate,
    SampleChainedChildFilter,
    SampleChainedChildUpdate,
    SampleChainedParent,
    SampleChainedParentCreate,
    SampleChainedParentUpdate,
    SampleModel,
    SampleSchemaFilter,
)


@pytest.mark.parametrize(
    "filter_type,expected_expression",
    [
        (FilterTypeEnum.EQUAL, lambda x, y: x == y),
        (FilterTypeEnum.NOT, lambda x, y: x != y),
        (FilterTypeEnum.IN, lambda x, y: x.in_(y)),
        (FilterTypeEnum.NOT_IN, lambda x, y: ~x.in_(y)),
        (FilterTypeEnum.LESS_THAN, lambda x, y: x < y),
        (FilterTypeEnum.LESS_THAN_OR_EQUAL, lambda x, y: x <= y),
        (FilterTypeEnum.GREATER_THAN, lambda x, y: x > y),
        (FilterTypeEnum.GREATER_THAN_OR_EQUAL, lambda x, y: x >= y),
    ],
)
def test_build_filter(filter_type, expected_expression, use_fixture_models):
    # Mock FilterSchemaType
    mock_filter = MagicMock()
    value = (
        ["mock_name"]
        if filter_type in {FilterTypeEnum.IN, FilterTypeEnum.NOT_IN}
        else "mock_name"
    )
    mock_filter.model_dump.return_value = {f"name__{filter_type.value}": value}

    # Mock Query
    mock_query = MagicMock(spec=Query)
    mock_query.filter.return_value = MagicMock(
        spec=Query
    )  # Return a new mock query for each filter() call

    store = StoreFilterMixin[SampleModel, SampleSchemaFilter](SampleModel)
    store.build_filter(mock_query, mock_filter, include_archived=True)

    # Check the correct function was called with the right arguments
    expected = expected_expression(SampleModel.name, value)
    call_strings = [str(call[0][0]) for call in mock_query.filter.call_args_list]
    assert str(expected) in call_strings


def test_build_filter_chain(clear_db, use_fixture_models):
    with get_db_context(refresh=True) as db_session:
        parent_store = StoreBase[
            SampleChainedParent, SampleChainedParentCreate, SampleChainedParentUpdate
        ](SampleChainedParent)
        child_store = StoreBase[
            SampleChainedChild, SampleChainedChildCreate, SampleChainedChildUpdate
        ](SampleChainedChild)
        child_filter_store = StoreFilterMixin[
            SampleChainedChild, SampleChainedChildFilter
        ](SampleChainedChild)

        parent1 = parent_store.create(
            db_session, obj_in=SampleChainedParentCreate(identifier="parent1")
        )
        parent2 = parent_store.create(
            db_session, obj_in=SampleChainedParentCreate(identifier="parent2")
        )

        child1 = child_store.create(
            db_session,
            obj_in=SampleChainedChildCreate(parent=parent1),
        )
        child2 = child_store.create(
            db_session,
            obj_in=SampleChainedChildCreate(parent=parent2),
        )

        parent_identifiers = child_filter_store.get_multi(
            db=db_session,
            filter=SampleChainedChildFilter(),
            only_fetch_columns=[
                chain_select(SampleChainedChild.parent)(SampleChainedParent.identifier)
            ],
        )
        parent_identifiers
        assert len(parent_identifiers) == 2
        assert parent_identifiers == [
            ("parent1",),
            ("parent2",),
        ]

    # Once the transaction is completed, we expect to see the parent IDs populated
    assert parent1.id
    assert parent2.id
    assert child1.parent_id == parent1.id
    assert child2.parent_id == parent2.id


def test_supports_all_filters():
    """
    All FilterSchemaType values defined in the enum are correctly parsed and supported
    in our build_filter method.

    """
    for filter_type in FilterTypeEnum:
        # Mock FilterSchemaType
        mock_filter = MagicMock()
        value = (
            ["mock_name"]
            if filter_type in {FilterTypeEnum.IN, FilterTypeEnum.NOT_IN}
            else "mock_name"
        )
        mock_filter.dict.return_value = {f"name__{filter_type.value}": value}

        # Mock Query
        mock_query = MagicMock(spec=Query)

        store = StoreFilterMixin[SampleModel, SampleSchemaFilter](SampleModel)
        assert (
            store.build_filter(mock_query, mock_filter, include_archived=True)
            is not None
        )
