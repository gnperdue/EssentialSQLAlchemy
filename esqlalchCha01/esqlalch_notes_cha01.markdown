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

How do we create relationships between tables? Association tables are used to
enable many-to-many relationships between two tables. A single `ForeignKey` on
a table is usually a sign of a one-to-many relationship. If there are mutltiple
`ForeignKey`s, there is a strong possibility the table is an association table.

Note that SQLAlchemy will only perform the resolution of a string to a table name
and column the first time it is accessed. If we used hard references, such as
`cookies.c.cookie_id` in our `ForeignKey` definitions, it will perform resolution
during module initialization. This could fail depending on the order in which
the tables are loaded.

## Persisting the Tables

Persisting the schema associated with our instance of `metadata` only requires
calling the `create_all()` method on it with the engine that should create
the tables. By default, it will not attempt to re-create tables that already
exist in the DB. In order to make changes or migrations, it is a good idea to
use a specialized tool like Alembic.

To set up the DB:

    MariaDB [(none)]> CREATE DATABASE essential_alchemy;
    Query OK, 1 row affected (0.00 sec)
    
    MariaDB [(none)]> SHOW DATABASES;
    +-------------------------------+
    | Database                      |
    +-------------------------------+
    ...
    | essential_alchemy             |
    ...
    +-------------------------------+
    16 rows in set (0.00 sec)

After running the code:

    MariaDB [(none)]> USE essential_alchemy
    Reading table information for completion of table and column names
    You can turn off this feature to get a quicker startup with -A
    
    Database changed
    MariaDB [essential_alchemy]> SHOW TABLES;
    +-----------------------------+
    | Tables_in_essential_alchemy |
    +-----------------------------+
    | cookies                     |
    | line_items                  |
    | orders                      |
    | users                       |
    +-----------------------------+
    4 rows in set (0.00 sec)
    
    MariaDB [essential_alchemy]> SHOW CREATE TABLE cookies\G
    *************************** 1. row ***************************
           Table: cookies
    Create Table: CREATE TABLE `cookies` (
      `cookie_id` int(11) NOT NULL AUTO_INCREMENT,
      `cookie_name` varchar(50) DEFAULT NULL,
      `cookie_recipe_url` varchar(255) DEFAULT NULL,
      `cookie_sku` varchar(55) DEFAULT NULL,
      `quantity` int(11) DEFAULT NULL,
      `unit_cost` decimal(12,2) DEFAULT NULL,
      PRIMARY KEY (`cookie_id`),
      KEY `ix_cookies_cookie_name` (`cookie_name`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    1 row in set (0.00 sec)
    
    MariaDB [essential_alchemy]> SHOW CREATE TABLE line_items\G
    *************************** 1. row ***************************
           Table: line_items
    Create Table: CREATE TABLE `line_items` (
      `line_items_id` int(11) NOT NULL AUTO_INCREMENT,
      `order_id` int(11) DEFAULT NULL,
      `cookie_id` int(11) DEFAULT NULL,
      `quantity` int(11) DEFAULT NULL,
      `extended_cost` decimal(12,2) DEFAULT NULL,
      PRIMARY KEY (`line_items_id`),
      KEY `order_id` (`order_id`),
      KEY `cookie_id` (`cookie_id`),
      CONSTRAINT `line_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
      CONSTRAINT `line_items_ibfk_2` FOREIGN KEY (`cookie_id`) REFERENCES `cookies` (`cookie_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    1 row in set (0.00 sec)
    
    MariaDB [essential_alchemy]> SHOW CREATE TABLE orders\G
    *************************** 1. row ***************************
           Table: orders
    Create Table: CREATE TABLE `orders` (
      `order_id` int(11) NOT NULL AUTO_INCREMENT,
      `user_id` int(11) DEFAULT NULL,
      `shipped` tinyint(1) DEFAULT NULL,
      PRIMARY KEY (`order_id`),
      KEY `user_id` (`user_id`),
      CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    1 row in set (0.00 sec)
    
    MariaDB [essential_alchemy]> SHOW CREATE TABLE users\G
    *************************** 1. row ***************************
           Table: users
    Create Table: CREATE TABLE `users` (
      `user_id` int(11) NOT NULL AUTO_INCREMENT,
      `username` varchar(15) NOT NULL,
      `email_address` varchar(255) NOT NULL,
      `phone` varchar(20) NOT NULL,
      `password` varchar(25) NOT NULL,
      `created_on` datetime DEFAULT NULL,
      `updated_on` datetime DEFAULT NULL,
      PRIMARY KEY (`user_id`),
      UNIQUE KEY `username` (`username`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    1 row in set (0.00 sec)

Hmmm, might have missed `customer_number` in `users` table... will skip for
now...
