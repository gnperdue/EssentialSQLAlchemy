# Schema and Types

SQLAlchemy needs a representation of the tables in the DB:

* user-defined `Table` objects
* declarative classes that represent tables
* inferring them from the DB

## Types

* generic
* SQL standard
* vendor specific
* user-defined

SQLAlchemy defines a large number of generic types that are abstracted away from
the specific backend. These may be found in `sqlalchemy.types`, and also in
`sqlalchemy`.

* `BigInteger`
* `Boolean` (== `BOOLEAN` or `SMALLINT`)
* `Date` (SQLite: `STRING`)
* `DateTime` (SQLite: `STRING`)
* `Enum` (== `ENUM` or `VARCHAR`)
* `Float`
* `Integer`
* `Interval`
* `LargeBinary` (== `BLOB`)
* `Numeric` (== `NUMERIC` or `DECIMAL`)
* `Unicode` (== `UNICODE` or `VARCHAR`)
* `Text` (== `CLOB` or `TEXT`)
* `Time` (== `DATETIME`)

Good examples of SQL and vendor specific types are `CHAR` and `NVARCHAR`, which
benefit from being the proper SQL type or types in databases from before
SQLAlchemy was created. The SQL standard types are available in `sqlalchemy.types`
in all caps. Vendor specific types may be found in `sqlalchemy.dialects`, again
in all caps.

## Metadata

Metadata acts as a sort of catalog of `Table` objects with information about the
engine and connection, and may be accessed via `MetaData.tables`.

    from sqlalchemy import MetaData
    metadata = MetaData()

## Tables

Tables are initialized in a supplied metadata object using the `Table` constructor.
Column objects represent each field in the table - they are the fundamental
building blocks. Note:

* we may mark primary keys
* we may specify indices

### Columns

Columns define the fields in a table and provide the primary means by which we
define other constraints through their keyword arguments. Different column types
feature different primary arguments. Also:

* may mark required
* force uniqueness
* set initial defaults

It is also possible to declare table constructs and constraints outisde of `Column`
objects. This is important when working with existing databases.

### Keys and Constraints

The objects representing keys and constraints are in the base SQLAlchemy module.
Three of the more common ones are:

* `PrimaryKeyConstraint`
* `UniqueConstraint`
* `CheckConstraint`

We may declare these in `Column` declarations, but we may also call them
separately, e.g.

    PrimaryKeyConstraint('user_id', name='user_pk')
    UniqueConstraint('username', name='uix_username')
    CheckConstraint('unit_cost >= 0.00', name='unit_cost_positive')

### Indexes

We may explicitly define an index with a construction type, e.g.

    from sqlalchemy import Index
    Index('ix_cookies_cookie_name', 'cookie_name')

We may also create functional indices that vary a bit by the backend database
being used. This allows us to create indices for situations that we need to
query often based on an unusual context, e.g., cooki SKU and name as a joined
item, such as `SKU0001 Chocolate Chip`. An index we might define for this lookup
is:

    Index('ix_test', mytable.c.cookie_sku, mytable.c.cookie_name)

### Relationships and `ForeignKeyConstraint`s

