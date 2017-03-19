# Exceptions and Transactions

## Exceptions

The most common errors are `AttributeErrors` and `IntegrityErrors`.

### `AttributeError`

`AttributeError`s occur when we attempt to access an attribute that doesn't
exist.

    In [1]: run attrib_error1.py
    ...
    2016-04-03 07:44:20,940 INFO sqlalchemy.engine.base.Engine SELECT users.username
    FROM users
    2016-04-03 07:44:20,940 INFO sqlalchemy.engine.base.Engine ()
    bruleboy
    ---------------------------------------------------------------------------
    AttributeError                            Traceback (most recent call last)
    /Users/gnperdue/Dropbox/Programming/Programming/Python/EssentialSQLAlchemy/esqlalchCha03/attrib_error1.py in <module>()
         20 for result in results:
         21     print(result.username)
    ---> 22     print(result.password)
    
    AttributeError: Could not locate column in row for column 'password'

Also,

    In [13]: s = select([cookies_tables.users.c.username,
        ...:             cookies_tables.users.c.hobby])
    ---------------------------------------------------------------------------
    AttributeError                            Traceback (most recent call last)

## `IntegrityError`

An `IntegrityError` occurs when we attempt to violate the constraints on a
`Column` or `Table`.

    In [2]: run attrib_error1.py
    2016-04-03 07:50:47,715 INFO sqlalchemy.engine.base.Engine INSERT INTO users (username, email_address, phone, password, created_on, updated_on) VALUES (%s, %s, %s, %s, %s, %s)
    2016-04-03 07:50:47,715 INFO sqlalchemy.engine.base.Engine ('bruleboy', 'bb@desert.org', '222-123-4444', 'firetruck!4evar', datetime.datetime(2016, 4, 3, 7, 50, 47, 715159), datetime.datetime(2016, 4, 3, 7, 50, 47, 715179))
    2016-04-03 07:50:47,716 INFO sqlalchemy.engine.base.Engine ROLLBACK
    ---------------------------------------------------------------------------
    IntegrityError                            Traceback (most recent call last)
    ...
    IntegrityError: (pymysql.err.IntegrityError) (1062, u"Duplicate entry 'bruleboy' for key 'username'") [SQL: u'INSERT INTO users (username, email_address, phone, password, created_on, updated_on) VALUES (%s, %s, %s, %s, %s, %s)'] [parameters: ('bruleboy', 'bb@desert.org', '222-123-4444', 'firetruck!4evar', datetime.datetime(2016, 4, 3, 7, 50, 47, 715159), datetime.datetime(2016, 4, 3, 7, 50, 47, 715179))]

Our output here is similar, but different to the book's - they have an error
message: "UNIQUE constraint failed:" that doesn't appear here. We do have
`unique=True` in the `Column` for `username` (but did not use a
`UniqueConstraint`).

Note that the traceback is not very interesting for `IntegrityError`s - there
is no syntax error - we are violating a database constraint, so the traceback is
only showing us the call stack for showing the error, etc.

### Handling Errors

    In [7]: run attrib_error2.py
    2016-04-03 08:01:49,580 INFO sqlalchemy.engine.base.Engine INSERT INTO users (username, email_address, phone, password, created_on, updated_on) VALUES (%s, %s, %s, %s, %s, %s)
    2016-04-03 08:01:49,580 INFO sqlalchemy.engine.base.Engine ('bruleboy', 'bb@desert.org', '222-123-4444', 'firetruck!4evar', datetime.datetime(2016, 4, 3, 8, 1, 49, 579986), datetime.datetime(2016, 4, 3, 8, 1, 49, 580009))
    2016-04-03 08:01:49,581 INFO sqlalchemy.engine.base.Engine ROLLBACK
    (pymysql.err.IntegrityError) (1062, u"Duplicate entry 'bruleboy' for key 'username'")
    ...

If we need multiple statements to succeed (and that depend on each other),
then wrapping individual statements in `try-except` blocks is inadequate.
We should use _transactions_.

## Transactions

Transactions are a way to ensure that groups of database statements either succeed
or fail all together as a unit. At the start of a transaction, we record the
current state of the db, then we execute multiple SQL statements. If they all
succeed, the database continues normally and we discard the prior state. However,
if even one fails, we catch the error and roll back to the saved state.

We will add a constraint to our databases to keep the number of cookies in
inventory non-negative. This probably means we need to re-create the tables.

* Go into MariaDB directly, `DROP TABLE table` all over the place (might
need to quit from IPython if we have a connection open).
* Run `fill_out_table.py` (sort of hacked together from previous scripts - not very
elegant).
* Well... the book wants different orders, so let's re-write `fill_out_table.py`
and fix it to look more like they want in this chapter...
* (Of course, actually, it might be silly to do this if running through a
second time since we have put the constraints into the table definitions
anyway...)

Okay, next we need to define the `ship_it` function...

    In [3]: run shipit1.py
    2016-04-30 13:00:19,997 INFO sqlalchemy.engine.base.Engine SELECT cookies.cookie_name, cookies.quantity
    FROM cookies
    2016-04-30 13:00:19,998 INFO sqlalchemy.engine.base.Engine ()
    ('chocolate chip', 12)
    ('dark chocolate chip', 1)
    ('white chocolate chip and macadamia nut', 1)
    ('peanut butter', 24)
    ('oatmeal raisin', 100)
    ...
    then, shipping it...
    ...
    then, again check the cookies
    ...
    ('chocolate chip', 3)
    ('dark chocolate chip', 1)
    ('white chocolate chip and macadamia nut', 1)
    ('peanut butter', 24)
    ('oatmeal raisin', 100)

Shouldn't we first check to see if the order has already been shipped, and, if
it hasn't, refuse to do the update?

We need to use exceptions to make it such that we only ship whole orders to
customers? **Transactions** provide a better way.

We initiate transactions by calling `begin()` on the connection object. The
result of the call is a transaction object we may use to control the results
of all our statements. If all of them succeed, we may call `commit()` on the
transaction object. If any fail, we call `rollback()` instead.

We may re-write `shipit()` to use transactions.

    In [4]: run shipit2.py
    2016-04-30 13:13:05,289 INFO sqlalchemy.engine.base.Engine SELECT cookies.cookie_name, cookies.quantity
    FROM cookies
    2016-04-30 13:13:05,289 INFO sqlalchemy.engine.base.Engine ()
    ('chocolate chip', 3)
    ('dark chocolate chip', 1)
    ('white chocolate chip and macadamia nut', 1)
    ('peanut butter', 24)
    ('oatmeal raisin', 100)
    ...
    after shipping it...
    ('chocolate chip', -6)
    ('dark chocolate chip', 1)
    ('white chocolate chip and macadamia nut', 1)
    ('peanut butter', 24)
    ('oatmeal raisin', 100)

Hmmm, well, it didn't stop the order for us because we must not have had the
proper constraint on the `cookies` table.

Try rebuilding the tables again. Go into MariaDB and drop them all...

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
    
    MariaDB [essential_alchemy]> DROP TABLE line_items;
    Query OK, 0 rows affected (0.01 sec)
    
    MariaDB [essential_alchemy]> DROP TABLE orders;
    Query OK, 0 rows affected (0.01 sec)
    
    MariaDB [essential_alchemy]> DROP TABLE users;
    Query OK, 0 rows affected (0.01 sec)

Some funny error/hang-up when dropping cookies... kill and try again.

    MariaDB [essential_alchemy]> DROP TABLE cookies;
    Query OK, 0 rows affected (10.32 sec)

Ah, problem must have been we had a transaction begun in Python, and we didn't
close it. (Quitting IPython made it possible to drop the table.)

So, looking at the db code, we have a constraint on quantity...

                CheckConstraint('quantity >= 0.00',
                                name='quantity_positive')

Why didn't it cause an integrity error? And... the reason is MariaDB and
MySQL don't support `CHECK` constraints.
