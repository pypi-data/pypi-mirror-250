# lassen

**40.4881° N, 121.5049° W**

Core utilities for MonkeySee web applications. Not guaranteed to be backwards compatible, use at your own risk.

At its core, Lassen tries to:

- Provide a suite of conventions for the 99% case of CRUD backends: manipulating data, storing it, and serving to frontends.
- Create typehinted definitions for everything to provide robust mypy support up and down the stack.
- Configure settings by environment variables, with a standard set of keys for database connections and web services.
- Make common things trivial and hard things possible.

We also build connective tissue between fast, more tailored libraries:

- FastAPI for webapp routes
- Pydantic for data validation
- SQLAlchemy for database management
- Alembic for database migrations

## Design Philosophy

Backends revolve around a core set of data objects. In the early days of design, these typically mirror the business objectives almost 1:1 (User, Team, Project). As complexity grows, they might also start to include auxiliary metadata, such as state enums or locally cached copies of other tables. These objects might be further optimized for the database engine: indexes, refactored foreign keys, etc. This creates a divergence between the data objects and the API that hosts it to the outside world.

In some ways database tables are like choosing the best data structure. They should efficiently move data from disk to memory to remote clients, and back again. So long as the data conversion is fast and lossless, it doesn't matter as much how the sausage is made.

A web API on the other hand aims to provide semantic objects to clients. These should be the objects and actions that represent your domain. The API layer should intentionally contrain the state/action space to be context aware. Useful APIs don't just mirror the database.

In Lassen, we view CRUD actions as projections on top of the underlying data objects. They might involve field merges, field subset, etc. Most libraries solve for this divergence by forcing a forking of class definitions: a separate definition to Create, to Update, etc. This often creates redundent code that's hard to sift through and reason about when adding new behavior.

Rather than configuring this CRUD at a class level, we focus on the CRUD actions that users can perform on each field. The `Stub` class defined below specifies _one_ key that is backed by a database value, and then generates CRUD schemas for API use depending on the allowed permissions for each field. Through this key-wise definition, we aim to clearly delineate in code and API contracts what is permitted, while aligning access patterns with the data values themselves.

## Structure

**Stores:** Each datamodel is expected to have its own store. Base classes that provide standard logic are provided by `lassen.store`
- StoreBase: Base class for all stores
- StoreFilterMixin: Mixin for filtering stores that specify an additional schema to use to filter
- StoreS3Mixin: Mixin for stores that use S3 for external storage of a piece of data. Support compression on both upload and downloads.

**Schemas:** Each datamodel should define a Model class (SQLAlchemy base object) and a series of Schema objects (Pydantic) that allow the Store to serialize the models. These schemas are also often used for direct CRUD referencing in the API layer.

We use a base `Stub` file to generate these schemas from a centralized definition. When defining generators you should use a path that can be fully managed by lassen, since we will remove and regenerate these files on each run.

```python
STORE_GENERATOR = StoreGenerator("models/auto")
SCHEMA_GENERATOR = SchemaGenerator("schemas/auto")
```

```bash
poetry run generate-lassen
```

**Migrations:** Lassen includes a templated alembic.init and env.py file. Client applications just need to have a `migrations` folder within their project root. After this you can swap `poetry run alembic` with `poetry run migrate`.

```sh
poetry run migrate upgrade head
```

**Settings:** Application settings should subclass our core settings. This provides a standard way to load settings from environment variables and includes common database keys.

```python
from lassen.core.config import CoreSettings, register_settings

@register_settings
class ClientSettings(CoreSettings):
    pass
```

**Schemas:** For helper schemas when returning results via API, see [lassen.schema](./lassen/schema.py).

## Development

Install all the extra dependencies so you can fully run the unit test suite.

```sh
poetry install --extras "aws database datasets"

createuser lassen
createdb -O lassen lassen_db
createdb -O lassen lassen_test_db
```

Unit Tests:

```sh
poetry run pytest
```
