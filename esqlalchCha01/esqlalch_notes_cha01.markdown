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


