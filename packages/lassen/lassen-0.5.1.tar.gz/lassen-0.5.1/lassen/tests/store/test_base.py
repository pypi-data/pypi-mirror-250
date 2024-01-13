from time import time

import pytest
from sqlalchemy.orm import Session

from lassen.store import StoreBase, StoreFilterMixin
from lassen.tests.model_fixtures import (
    SampleModel,
    SampleSchemaCreate,
    SampleSchemaFilter,
    SampleSchemaUpdate,
)


def create_batch(db_session: Session, quantity: int = 1):
    created_objects = []
    for i in range(quantity):
        test_model = SampleModel(name=f"Test Model {i}")
        db_session.add(test_model)
        created_objects.append(test_model)

    db_session.commit()

    for obj in created_objects:
        db_session.refresh(obj)

    return [obj.id for obj in created_objects]


def test_store_base_get(db_session: Session, use_fixture_models):
    test_model_id = create_batch(db_session, quantity=1)[0]

    store = StoreBase[SampleModel, SampleSchemaCreate, SampleSchemaUpdate](SampleModel)
    # Test with a valid ID
    retrieved = store.get(db_session, id=test_model_id)
    assert retrieved is not None
    assert retrieved.id == test_model_id
    assert retrieved.name == "Test Model 0"

    # Test with an invalid ID
    assert store.get(db_session, id=9999) is None


def test_store_base_get_multi(db_session: Session, use_fixture_models):
    create_batch(db_session, quantity=5)

    store = StoreFilterMixin[SampleModel, SampleSchemaFilter](SampleModel)
    # Test without skip and limit
    retrieved = store.get_multi(db_session, filter=SampleSchemaFilter())
    assert len(retrieved) == 5

    # Test with skip
    retrieved = store.get_multi(db_session, skip=2, filter=SampleSchemaFilter())
    assert len(retrieved) == 3

    # Test with limit
    retrieved = store.get_multi(db_session, limit=2, filter=SampleSchemaFilter())
    assert len(retrieved) == 2

    # Test with skip and limit
    retrieved = store.get_multi(
        db_session, skip=1, limit=2, filter=SampleSchemaFilter()
    )
    assert len(retrieved) == 2


def test_store_base_create(db_session: Session, use_fixture_models):
    store = StoreBase[SampleModel, SampleSchemaCreate, SampleSchemaUpdate](SampleModel)
    create_schema = SampleSchemaCreate(name="Test Name")
    created = store.create(db_session, obj_in=create_schema)
    db_session.commit()
    assert created.id is not None
    assert created.name == "Test Name"


BULK_CREATE_PARAMS = [
    (50, 0.1, 100),
    # (50000, 4.5, 100),
    # (50000, 5.0, 1000),
]


@pytest.mark.parametrize("quantity,expected_max_time,batch_size", BULK_CREATE_PARAMS)
def test_store_bulk_create(
    quantity: int,
    expected_max_time: float,
    batch_size: int,
    db_session: Session,
    use_fixture_models,
):
    store = StoreBase[SampleModel, SampleSchemaCreate, SampleSchemaUpdate](SampleModel)

    start = time()
    store.bulk_create(
        db_session,
        [SampleSchemaCreate(name=f"Inserted Name {i}") for i in range(quantity)],
        batch_size=batch_size,
    )
    end = time()

    assert end - start < expected_max_time

    filter_store = StoreFilterMixin[SampleModel, SampleSchemaFilter](SampleModel)
    all_schemas = filter_store.get_multi(db_session, filter=SampleSchemaFilter())
    assert len(all_schemas) == quantity

    schema_names = {schema.name for schema in all_schemas}
    assert {f"Inserted Name {i}" for i in range(quantity)} == schema_names


@pytest.mark.parametrize("quantity,expected_max_time,batch_size", BULK_CREATE_PARAMS)
@pytest.mark.asyncio
async def test_store_bulk_create_async(
    quantity: int,
    expected_max_time: float,
    batch_size: int,
    db_session: Session,
    use_fixture_models,
):
    store = StoreBase[SampleModel, SampleSchemaCreate, SampleSchemaUpdate](SampleModel)

    fixed_schemas = [
        SampleSchemaCreate(name=f"Inserted Name {i}") for i in range(quantity)
    ]

    async def async_schemas():
        for schema in fixed_schemas:
            yield schema

    start = time()
    await store.bulk_create_async(
        db_session,
        async_schemas(),
        batch_size=batch_size,
    )
    end = time()

    assert end - start < expected_max_time

    filter_store = StoreFilterMixin[SampleModel, SampleSchemaFilter](SampleModel)
    all_schemas = filter_store.get_multi(db_session, filter=SampleSchemaFilter())
    assert len(all_schemas) == quantity

    schema_names = {schema.name for schema in all_schemas}
    assert {f"Inserted Name {i}" for i in range(quantity)} == schema_names


def test_store_base_update(db_session: Session, use_fixture_models):
    test_model_id = create_batch(db_session, quantity=1)[0]

    store = StoreBase[SampleModel, SampleSchemaCreate, SampleSchemaUpdate](SampleModel)
    update_schema = SampleSchemaUpdate(name="Updated Name")
    db_obj = store.get(db_session, id=test_model_id)
    assert db_obj is not None

    updated = store.update(db_session, db_obj=db_obj, obj_in=update_schema)
    db_session.commit()
    assert updated.id == test_model_id
    assert updated.name == "Updated Name"


BULK_UPDATE_PARAMS = [
    (50, 0.1, 100),
    # (5000, 2.0, 100),
    # (50000, 20.0, 100),
    # (50000, 20.0, 1000),
]


@pytest.mark.parametrize(
    "quantity,expected_max_time,batch_size",
    BULK_UPDATE_PARAMS,
)
def test_store_bulk_update(
    quantity: int,
    expected_max_time: float,
    batch_size: int,
    db_session: Session,
    use_fixture_models,
):
    test_model_ids = create_batch(db_session, quantity=quantity)
    assert len(test_model_ids) == quantity

    store = StoreBase[SampleModel, SampleSchemaCreate, SampleSchemaUpdate](SampleModel)

    start = time()
    store.bulk_update(
        db_session,
        [
            (model_id, SampleSchemaUpdate(name=f"Updated Name {i}"))
            for i, model_id in enumerate(test_model_ids)
        ],
        batch_size=batch_size,
    )
    end = time()
    assert end - start < expected_max_time

    filter_store = StoreFilterMixin[SampleModel, SampleSchemaFilter](SampleModel)
    all_models = {
        model.id: model
        for model in filter_store.get_multi(db_session, filter=SampleSchemaFilter())
    }

    for i, model_id in enumerate(test_model_ids):
        updated = all_models[model_id]
        assert updated
        assert updated.id == model_id
        assert updated.name == f"Updated Name {i}"


@pytest.mark.parametrize(
    "quantity,expected_max_time,batch_size",
    BULK_UPDATE_PARAMS,
)
@pytest.mark.asyncio
async def test_store_bulk_update_async(
    quantity: int,
    expected_max_time: float,
    batch_size: int,
    db_session: Session,
    use_fixture_models,
):
    test_model_ids = create_batch(db_session, quantity=quantity)
    assert len(test_model_ids) == quantity

    store = StoreBase[SampleModel, SampleSchemaCreate, SampleSchemaUpdate](SampleModel)

    async def update_schemas():
        for i, model_id in enumerate(test_model_ids):
            yield model_id, SampleSchemaUpdate(name=f"Updated Name {i}")

    start = time()
    await store.bulk_update_async(
        db_session,
        update_schemas(),
        batch_size=batch_size,
    )
    end = time()
    assert end - start < expected_max_time

    filter_store = StoreFilterMixin[SampleModel, SampleSchemaFilter](SampleModel)
    all_models = {
        model.id: model
        for model in filter_store.get_multi(db_session, filter=SampleSchemaFilter())
    }

    for i, model_id in enumerate(test_model_ids):
        updated = all_models[model_id]
        assert updated
        assert updated.id == model_id
        assert updated.name == f"Updated Name {i}"


def test_store_base_remove(db_session: Session, use_fixture_models):
    test_model_id = create_batch(db_session, quantity=1)[0]

    store = StoreBase[SampleModel, SampleSchemaCreate, SampleSchemaUpdate](SampleModel)
    store.remove(db_session, id=test_model_id)
    db_session.commit()

    # Test that the model instance has been removed
    assert store.get(db_session, id=test_model_id) is None
