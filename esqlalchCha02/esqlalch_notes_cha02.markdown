# Working with Data via SQLAlchemy Core

## Inserting Data

We use the `insert()` method on a `Table` to insert data

    In [2]: run inserting_data.py
    2016-02-22 20:50:49,202 INFO sqlalchemy.engine.base.Engine SHOW VARIABLES LIKE 'sql_mode'
    2016-02-22 20:50:49,202 INFO sqlalchemy.engine.base.Engine ()
    2016-02-22 20:50:49,209 INFO sqlalchemy.engine.base.Engine SELECT DATABASE()
    2016-02-22 20:50:49,209 INFO sqlalchemy.engine.base.Engine ()
    2016-02-22 20:50:49,212 INFO sqlalchemy.engine.base.Engine show collation where `Charset` = 'utf8' and `Collation` = 'utf8_bin'
    2016-02-22 20:50:49,212 INFO sqlalchemy.engine.base.Engine ()
    2016-02-22 20:50:49,214 INFO sqlalchemy.engine.base.Engine SELECT CAST('test plain returns' AS CHAR(60)) AS anon_1
    2016-02-22 20:50:49,214 INFO sqlalchemy.engine.base.Engine ()
    2016-02-22 20:50:49,216 INFO sqlalchemy.engine.base.Engine SELECT CAST('test unicode returns' AS CHAR(60)) AS anon_1
    2016-02-22 20:50:49,216 INFO sqlalchemy.engine.base.Engine ()
    2016-02-22 20:50:49,217 INFO sqlalchemy.engine.base.Engine SELECT CAST('test collated returns' AS CHAR CHARACTER SET utf8) COLLATE utf8_bin AS anon_1
    2016-02-22 20:50:49,217 INFO sqlalchemy.engine.base.Engine ()
    2016-02-22 20:50:49,219 INFO sqlalchemy.engine.base.Engine DESCRIBE `line_items`
    2016-02-22 20:50:49,219 INFO sqlalchemy.engine.base.Engine ()
    2016-02-22 20:50:49,227 INFO sqlalchemy.engine.base.Engine DESCRIBE `cookies`
    2016-02-22 20:50:49,227 INFO sqlalchemy.engine.base.Engine ()
    2016-02-22 20:50:49,232 INFO sqlalchemy.engine.base.Engine DESCRIBE `users`
    2016-02-22 20:50:49,232 INFO sqlalchemy.engine.base.Engine ()
    2016-02-22 20:50:49,236 INFO sqlalchemy.engine.base.Engine DESCRIBE `orders`
    2016-02-22 20:50:49,237 INFO sqlalchemy.engine.base.Engine ()
    INSERT INTO cookies (cookie_name, cookie_recipe_url, cookie_sku, quantity, unit_cost) VALUES (:cookie_name, :cookie_recipe_url, :cookie_sku, :quantity, :unit_cost).

Our supplied values have been repalced with `:column_name`, which is how
SQLAlchemy represents parameters displayed via `str()`. These parameters are used
to help ensure our data has been properly escaped to mitigate the risk of SQL
injection attacks. We may still view the parameters by looking at the compiled
version of the statement.

    In [3]: ins
    Out[3]: <sqlalchemy.sql.dml.Insert object at 0x104313a50>
    
    In [4]: ins.compile().params
    Out[4]:
    {'cookie_name': 'chocolate chip',
     'cookie_recipe_url': 'http://some.aweso.me/cookie/recipe.html',
     'cookie_sku': 'CC01',
     'quantity': '12',
     'unit_cost': '0.50'}

    In [6]: result = connection.execute(ins)
    2016-02-24 21:25:16,541 INFO sqlalchemy.engine.base.Engine INSERT INTO cookies (cookie_name, cookie_recipe_url, cookie_sku, quantity, unit_cost) VALUES (%s, %s, %s, %s, %s)
    2016-02-24 21:25:16,541 INFO sqlalchemy.engine.base.Engine ('chocolate chip', 'http://some.aweso.me/cookie/recipe.html', 'CC01', '12', '0.50')
    2016-02-24 21:25:16,550 INFO sqlalchemy.engine.base.Engine COMMIT

    MariaDB [essential_alchemy]> SELECT * FROM cookies\G
    *************************** 1. row ***************************
            cookie_id: 1
          cookie_name: chocolate chip
    cookie_recipe_url: http://some.aweso.me/cookie/recipe.html
           cookie_sku: CC01
             quantity: 12
            unit_cost: 0.50
    1 row in set (0.00 sec)

What we have actually been doing is building a tree-like structure that can be
quickly traversed. When we call `execute()`, it is compiled into the proper
database dialect and sent to the DB.

    In [7]: result
    Out[7]: <sqlalchemy.engine.result.ResultProxy at 0x10416e510>
    
    In [8]: result.
    result.close                         result.last_updated_params
    result.closed                        result.lastrow_has_defaults
    result.connection                    result.lastrowid
    result.context                       result.out_parameters
    result.cursor                        result.postfetch_cols
    result.dialect                       result.prefetch_cols
    result.fetchall                      result.process_rows
    result.fetchmany                     result.returned_defaults
    result.fetchone                      result.returns_rows
    result.first                         result.rowcount
    result.inserted_primary_key          result.scalar
    result.is_insert                     result.supports_sane_multi_rowcount
    result.keys                          result.supports_sane_rowcount
    result.last_inserted_params

In addition to having insert as a method of a `Table` object, it is also
available as a top-level function.

    In [9]: run inserting_data2.py
    
    In [10]: ins.compile().params
    Out[10]:
    {'cookie_name': 'white chocolate chip and macadamia nut',
     'cookie_recipe_url': 'http://some.aweso.me/cookie/white_choc_maca_nut.html',
     'cookie_sku': 'CC03',
     'quantity': '1',
     'unit_cost': '1.00'}
    
    In [11]: result = connection.execute(ins)
    2016-02-24 21:35:54,633 INFO sqlalchemy.engine.base.Engine INSERT INTO cookies (cookie_name, cookie_recipe_url, cookie_sku, quantity, unit_cost) VALUES (%s, %s, %s, %s, %s)
    2016-02-24 21:35:54,634 INFO sqlalchemy.engine.base.Engine ('white chocolate chip and macadamia nut', 'http://some.aweso.me/cookie/white_choc_maca_nut.html', 'CC03', '1', '1.00')
    2016-02-24 21:35:54,635 INFO sqlalchemy.engine.base.Engine COMMIT


    MariaDB [essential_alchemy]> SELECT * FROM cookies WHERE cookie_id > 1\G
    *************************** 1. row ***************************
            cookie_id: 2
          cookie_name: white chocolate chip and macadamia nut
    cookie_recipe_url: http://some.aweso.me/cookie/white_choc_maca_nut.html
           cookie_sku: CC03
             quantity: 1
            unit_cost: 1.00
    1 row in set (0.00 sec)

The `execute()` method of the `connection` object may take more than just
statements. We may also provide values as keyword arguments after the
statement.

    In [12]: run inserting_data3.py
    2016-02-24 21:51:18,687 INFO sqlalchemy.engine.base.Engine INSERT INTO cookies (cookie_name, cookie_recipe_url, cookie_sku, quantity, unit_cost) VALUES (%s, %s, %s, %s, %s)
    2016-02-24 21:51:18,687 INFO sqlalchemy.engine.base.Engine ('dark chocolate chip', 'http://some.aweso.me/cookie/recipe_dark.html', 'CC02', '1', '0.75')
    2016-02-24 21:51:18,688 INFO sqlalchemy.engine.base.Engine COMMIT
    
    MariaDB [essential_alchemy]> SELECT * FROM cookies WHERE cookie_id = 3\G
    *************************** 1. row ***************************
            cookie_id: 3
          cookie_name: dark chocolate chip
    cookie_recipe_url: http://some.aweso.me/cookie/recipe_dark.html
           cookie_sku: CC02
             quantity: 1
            unit_cost: 0.75
    1 row in set (0.01 sec)

We may also insert multiple records at once by using a list of dictionaries.

    In [13]: run inserting_data4.py
    2016-02-24 21:56:43,323 INFO sqlalchemy.engine.base.Engine INSERT INTO cookies (cookie_name, cookie_recipe_url, cookie_sku, quantity, unit_cost) VALUES (%s, %s, %s, %s, %s)
    2016-02-24 21:56:43,323 INFO sqlalchemy.engine.base.Engine (('peanut butter', 'http://some.aweso.me/cookie/peanut.html', 'PB01', '24', '0.25'), ('oatmeal raisin', 'http://some.aweso.me/cookie/raisin.html', 'EWW01', '100', '1.00'))
    2016-02-24 21:56:43,324 INFO sqlalchemy.engine.base.Engine COMMIT

SQLAlchemy will compile the statement against the first dictionary in the list, so
they must all have the same keys.

## Querying Data

We may use the `select()` function, which is analogous to the SQL `SELECT`:

    In [2]: run select1.py
    2016-02-26 21:34:10,640 INFO sqlalchemy.engine.base.Engine SELECT cookies.cookie_id, cookies.cookie_name, cookies.cookie_recipe_url, cookies.cookie_sku, cookies.quantity, cookies.unit_cost
    FROM cookies
    2016-02-26 21:34:10,640 INFO sqlalchemy.engine.base.Engine ()
    [(1, 'chocolate chip', 'http://some.aweso.me/cookie/recipe.html', 'CC01', 12, Decimal('0.50')), (2, 'white chocolate chip and macadamia nut', 'http://some.aweso.me/cookie/white_choc_maca_nut.html', 'CC03', 1, Decimal('1.00')), (3, 'dark chocolate chip', 'http://some.aweso.me/cookie/recipe_dark.html', 'CC02', 1, Decimal('0.75')), (4, 'peanut butter', 'http://some.aweso.me/cookie/peanut.html', 'PB01', 24, Decimal('0.25')), (5, 'oatmeal raisin', 'http://some.aweso.me/cookie/raisin.html', 'EWW01', 100, Decimal('1.00'))]

`select()` expects a list of columns; but, for convenience, it also accepts `Table`
objects and selects all the columns in the `Table`. We may also use the `select`
method on the `Table` object.

    In [3]: run select2.py
    2016-02-26 21:37:48,521 INFO sqlalchemy.engine.base.Engine SELECT cookies.cookie_id, cookies.cookie_name, cookies.cookie_recipe_url, cookies.cookie_sku, cookies.quantity, cookies.unit_cost
    FROM cookies
    2016-02-26 21:37:48,521 INFO sqlalchemy.engine.base.Engine ()
    [(1, 'chocolate chip', 'http://some.aweso.me/cookie/recipe.html', 'CC01', 12, Decimal('0.50')), (2, 'white chocolate chip and macadamia nut', 'http://some.aweso.me/cookie/white_choc_maca_nut.html', 'CC03', 1, Decimal('1.00')), (3, 'dark chocolate chip', 'http://some.aweso.me/cookie/recipe_dark.html', 'CC02', 1, Decimal('0.75')), (4, 'peanut butter', 'http://some.aweso.me/cookie/peanut.html', 'PB01', 24, Decimal('0.25')), (5, 'oatmeal raisin', 'http://some.aweso.me/cookie/raisin.html', 'EWW01', 100, Decimal('1.00'))]

### `ResultProxy`

A `ResultProxy` is a wrapper around a DBAPI cursor object and it is meant to make
it simpler to use and manipulate the results of a statement. With `results` from
`select2.py`:

    In [4]: results[0]
    Out[4]: (1, 'chocolate chip', 'http://some.aweso.me/cookie/recipe.html', 'CC01', 12, Decimal('0.50'))
    
    In [5]: first_row = results[0]
    
    In [6]: first_row[1]
    Out[6]: 'chocolate chip'
    
    In [7]: first_row.cookie_name
    Out[7]: 'chocolate chip'
    
    In [8]: first_row[cookies_tables.cookies.c.cookie_name]
    Out[8]: 'chocolate chip'

We may also iterate over `ResultsProxy`s... Still working with objects from
`select2.py`:

    In [13]: s = cookies_tables.cookies.select()
    
    In [14]: rp = connection.execute(s)
    2016-02-26 21:42:19,871 INFO sqlalchemy.engine.base.Engine SELECT cookies.cookie_id, cookies.cookie_name, cookies.cookie_recipe_url, cookies.cookie_sku, cookies.quantity, cookies.unit_cost
    FROM cookies
    2016-02-26 21:42:19,872 INFO sqlalchemy.engine.base.Engine ()
    
    In [15]: for record in rp:
       ....:     print(record.cookie_name)
       ....:
    chocolate chip
    white chocolate chip and macadamia nut
    dark chocolate chip
    peanut butter
    oatmeal raisin

Note that if we now call `fetcall()`, the result is empty:

    In [16]: rp.fetchall()
    Out[16]: []

We can use all the following methods to fetch results:

* `first()` - get the first if it exists and then close the connection
* `fetchone()` - returns one row and leaves the cursor open for additional calls
* `scalar()` - returns a single valueif a query results in a single record with
one column
* `keys()` will get a list of the column names.

For example:

    In [17]: rp = connection.execute(s)
    2016-02-26 21:46:47,809 INFO sqlalchemy.engine.base.Engine SELECT cookies.cookie_id, cookies.cookie_name, cookies.cookie_recipe_url, cookies.cookie_sku, cookies.quantity, cookies.unit_cost
    FROM cookies
    2016-02-26 21:46:47,810 INFO sqlalchemy.engine.base.Engine ()
    
    In [18]: rp.keys()
    Out[18]:
    ['cookie_id',
     'cookie_name',
     'cookie_recipe_url',
     'cookie_sku',
     'quantity',
     'unit_cost']

**Tips** for good production code:

* use `first()` for getting a single record in preference to `fetchone()` or
`scalar()`
* prefer the iterable over `fetchall()` and `fetchone()` - it is more memory
efficient
* avoid `fetchone()` - it leaves connections open
* use `scalar()` sparingly - it raises errors if a query returns more than one
row with one column

Often, we only need a portion of the columns...

### Controlling the Columns in the Query

    In [19]: run select3.py
    2016-02-26 21:52:31,777 INFO sqlalchemy.engine.base.Engine SELECT cookies.cookie_name, cookies.quantity
    FROM cookies
    2016-02-26 21:52:31,777 INFO sqlalchemy.engine.base.Engine ()
    ['cookie_name', 'quantity']
    ('chocolate chip', 12)

    ... restart session ...

    In [2]: result
    Out[2]: ('chocolate chip', 12)
    
    In [3]: type(result)
    Out[3]: sqlalchemy.engine.result.RowProxy
    
    In [4]: result[0]
    Out[4]: 'chocolate chip'
    
    In [5]: result[-1]
    ---------------------------------------------------------------------------
    NoSuchColumnError: "Could not locate column in row for column '-1'"
    
    In [6]: result[1]
    Out[6]: 12
    
    In [7]: result[0:1]
    Out[7]: ('chocolate chip',)
    
    In [8]: result[0:2]
    Out[8]: ('chocolate chip', 12)

### Ordering

We may call `order_by()` on our select:

    In [9]: run select4.py
    2016-02-27 09:05:53,763 INFO sqlalchemy.engine.base.Engine SELECT cookies.cookie_name, cookies.quantity
    FROM cookies ORDER BY cookies.quantity
    2016-02-27 09:05:53,763 INFO sqlalchemy.engine.base.Engine ()
    1 - white chocolate chip and macadamia nut
    1 - dark chocolate chip
    12 - chocolate chip
    24 - peanut butter
    100 - oatmeal raisin

We may also use descending order:

    ... restarting the session ...
    In [1]: run select5.py
    2016-02-28 05:53:17,901 INFO sqlalchemy.engine.base.Engine SHOW VARIABLES LIKE 'sql_mode'
    2016-02-28 05:53:17,901 INFO sqlalchemy.engine.base.Engine ()
    2016-02-28 05:53:17,903 INFO sqlalchemy.engine.base.Engine SELECT DATABASE()
    ...
    2016-02-28 05:53:17,924 INFO sqlalchemy.engine.base.Engine SELECT cookies.cookie_name, cookies.quantity
    FROM cookies ORDER BY cookies.quantity DESC
    2016-02-28 05:53:17,924 INFO sqlalchemy.engine.base.Engine ()
    100 - oatmeal raisin
    24 - peanut butter
    12 - chocolate chip
    1 - white chocolate chip and macadamia nut
    1 - dark chocolate chip

### Limiting

While we may use `ResultProxy` to get the `first()` or one (via `fetchone()`)
result, the actual query ran over and accessed all the results. To limit the
query, we must use the `limit()` function.

    In [2]: run limit1.py
    2016-02-28 05:56:52,105 INFO sqlalchemy.engine.base.Engine SELECT cookies.cookie_name, cookies.quantity
    FROM cookies ORDER BY cookies.quantity
     LIMIT %s
    2016-02-28 05:56:52,105 INFO sqlalchemy.engine.base.Engine (2,)
    1 - white chocolate chip and macadamia nut
    1 - dark chocolate chip

### Built-in SQL Functions and Labels

SQLAlchemy can also leverage SQL functions on the DB backend. To use functions
like `SUM()` and `COUNT()` we need to import `sqlalchemy.sql.func`. The functions
are wrapped around the columns on which they operate.

    In [3]: run sqlfunc1.py
    2016-02-28 06:29:07,125 INFO sqlalchemy.engine.base.Engine SELECT sum(cookies.quantity) AS sum_1
    FROM cookies
    2016-02-28 06:29:07,125 INFO sqlalchemy.engine.base.Engine ()
    138
    
    MariaDB [essential_alchemy]> SELECT sum(cookies.quantity) AS sum_1 FROM cookies;
    +-------+
    | sum_1 |
    +-------+
    |   138 |
    +-------+
    1 row in set (0.00 sec)

And,

    In [6]: run sqlfunc2.py
    2016-02-28 17:08:47,905 INFO sqlalchemy.engine.base.Engine SELECT count(cookies.cookie_name) AS count_1
    FROM cookies
    2016-02-28 17:08:47,905 INFO sqlalchemy.engine.base.Engine ()
    [u'count_1']
    5

    MariaDB [essential_alchemy]> SELECT count(cookies.cookie_name) AS count_1
        -> FROM cookies;
    +---------+
    | count_1 |
    +---------+
    |       5 |
    +---------+
    1 row in set (0.00 sec)

We can make the result a bit more clear with the `label()` function:

    In [2]: run sqlfunc3.py
    2016-03-02 21:07:25,438 INFO sqlalchemy.engine.base.Engine SELECT count(cookies.cookie_name) AS inventory_count
    FROM cookies
    2016-03-02 21:07:25,438 INFO sqlalchemy.engine.base.Engine ()
    ['inventory_count']
    5

### Filtering

Filtering queries is done with `where()` statements. Usually, a `where()` clause
has a column, an operator, and a value or column. We may chain multiple `where()`
clauses together and they act like `AND`s in SQL statements.

    In [4]: run filtering1.py
    2016-03-02 21:11:02,769 INFO sqlalchemy.engine.base.Engine SELECT cookies.cookie_id, cookies.cookie_name, cookies.cookie_recipe_url, cookies.cookie_sku, cookies.quantity, cookies.unit_cost
    FROM cookies
    WHERE cookies.cookie_name = %s
    2016-03-02 21:11:02,770 INFO sqlalchemy.engine.base.Engine ('chocolate chip',)
    [('cookie_id', 1), ('cookie_name', 'chocolate chip'), ('cookie_recipe_url', 'http://some.aweso.me/cookie/recipe.html'), ('cookie_sku', 'CC01'), ('quantity', 12), ('unit_cost', Decimal('0.50'))]

We can also use `like()`:

    In [5]: run filtering2.py
    2016-03-02 21:30:34,417 INFO sqlalchemy.engine.base.Engine SELECT cookies.cookie_id, cookies.cookie_name, cookies.cookie_recipe_url, cookies.cookie_sku, cookies.quantity, cookies.unit_cost
    FROM cookies
    WHERE cookies.cookie_name LIKE %s
    2016-03-02 21:30:34,417 INFO sqlalchemy.engine.base.Engine ('%chocolate chip%',)
    chocolate chip
    white chocolate chip and macadamia nut
    dark chocolate chip

### `ClauseElement`s

`ClauseElement`s are entities we use in clauses, typically columns in a table.
Unlike columns though, `ClauseElements` have many additional capabilities.
Examples include:

* `between(cleft, cright)`
* `concat(column_two)`
* `distinct()`
* `in_([list])`
* `is_(None)`
* `contains(<string>)`
* `endswith(<string>)`
* `like(<string>)`
* `startswith(<string>)`
* `ilike(<string>)`

There are also negative versions of these methods, e.g. `notlike` and `notin_()`.
The only exception to the naming pattern is `isnot()`, which drops the
underscore.

### Operators

We may use many operators to filter data. We have standard comparison operators,
`==`, `!=`, `<`, `>`, `<=`, `>=`. If `==` is compared to `None`, it is converted
to an `IS NULL` statement. Arithmetic operators are also supported, e.g., `+`,
`-`, `*`, `/`, and `%` with database-independent capabilities for string
concatenation (`\+`), etc.

    In [1]: run operators1.py
    2016-03-04 18:56:11,378 INFO sqlalchemy.engine.base.Engine SHOW VARIABLES LIKE 'sql_mode'
    2016-03-04 18:56:11,378 INFO sqlalchemy.engine.base.Engine ()
    ...
    2016-03-04 18:56:11,412 INFO sqlalchemy.engine.base.Engine SELECT cookies.cookie_name, concat(%s, cookies.cookie_sku) AS anon_1
    FROM cookies
    2016-03-04 18:56:11,412 INFO sqlalchemy.engine.base.Engine ('SKU-',)
    ('chocolate chip', 'SKU-CC01')
    ('white chocolate chip and macadamia nut', 'SKU-CC03')
    ('dark chocolate chip', 'SKU-CC02')
    ('peanut butter', 'SKU-PB01')
    ('oatmeal raisin', 'SKU-EWW01')

Another common use it to compute values from multiple columns.

    In [3]: run operators2.py
    2016-03-04 19:01:07,593 INFO sqlalchemy.engine.base.Engine SELECT cookies.cookie_name, CAST(cookies.quantity * cookies.unit_cost AS DECIMAL(12, 2)) AS inv_cost
    FROM cookies
    2016-03-04 19:01:07,593 INFO sqlalchemy.engine.base.Engine ()
    chocolate chip - 6.00
    white chocolate chip and macadamia nut - 1.00
    dark chocolate chip - 0.75
    peanut butter - 6.00
    oatmeal raisin - 100.00

### Boolean Operators

SQLAlchemy also has `AND`, `OR`, and `NOT` via `&`, `|`, and `~`. Special care
must be taken with these due to Python's operator precedence rules. So, `&`
binds more closely than `<`, so `A < B & C < D` really means `A < (B&C) < D`
even though you may have meant `(A < B) & (C < D)`. Conjuctions are better than
these overloads. Conjuctions also let us handle multiple chained `where()`
clauses.

### Conjunctions

Conjunctions in SQLAlchemcy are `and_()`, `or_()`, and `not_()`.

    In [5]: run conjunctions1.py
    2016-03-04 19:18:15,117 INFO sqlalchemy.engine.base.Engine SELECT cookies.cookie_id, cookies.cookie_name, cookies.cookie_recipe_url, cookies.cookie_sku, cookies.quantity, cookies.unit_cost
    FROM cookies
    WHERE cookies.quantity > %s AND cookies.unit_cost < %s
    2016-03-04 19:18:15,118 INFO sqlalchemy.engine.base.Engine (23, 0.4)
    peanut butter

    In [6]: run conjunctions2.py
    2016-03-04 19:20:00,578 INFO sqlalchemy.engine.base.Engine SELECT cookies.cookie_id, cookies.cookie_name, cookies.cookie_recipe_url, cookies.cookie_sku, cookies.quantity, cookies.unit_cost
    FROM cookies
    WHERE cookies.quantity BETWEEN %s AND %s OR (cookies.cookie_name LIKE concat(concat('%%', %s), '%%'))
    2016-03-04 19:20:00,578 INFO sqlalchemy.engine.base.Engine (10, 50, 'chip')
    chocolate chip
    white chocolate chip and macadamia nut
    dark chocolate chip
    peanut butter

## Updating Data

Updates are very similar to inserts - except we use `where` to specify which
rows to change.

    In [7]: run updatingdata1.py
    2016-03-04 19:25:48,866 INFO sqlalchemy.engine.base.Engine UPDATE cookies SET quantity=(cookies.quantity + %s) WHERE cookies.cookie_name = %s
    2016-03-04 19:25:48,866 INFO sqlalchemy.engine.base.Engine (120, 'chocolate chip')
    2016-03-04 19:25:48,876 INFO sqlalchemy.engine.base.Engine COMMIT
    1
    2016-03-04 19:25:48,878 INFO sqlalchemy.engine.base.Engine SELECT cookies.cookie_id, cookies.cookie_name, cookies.cookie_recipe_url, cookies.cookie_sku, cookies.quantity, cookies.unit_cost
    FROM cookies
    WHERE cookies.cookie_name = %s
    2016-03-04 19:25:48,879 INFO sqlalchemy.engine.base.Engine ('chocolate chip',)
               cookie_id: 1
             cookie_name: chocolate chip
       cookie_recipe_url: http://some.aweso.me/cookie/recipe.html
              cookie_sku: CC01
                quantity: 132
               unit_cost: 0.50

## Deleting Data

We may use either the `delete()` function or the `delete()` `Table` method.
`delete` takes no values parameter - only an optional `where` clause (which, if
omitted, will cause all rows in the table to be deleted).

## Joins

We use `join()` and `outerjoin()` to query related data.

    In [2]: run joins1.py
    2016-03-15 22:02:58,472 INFO sqlalchemy.engine.base.Engine SELECT orders.order_id, users.username, users.phone, cookies.cookie_name, line_items.quantity, line_items.extended_cost
    FROM orders INNER JOIN users ON users.user_id = orders.user_id INNER JOIN line_items ON orders.order_id = line_items.order_id INNER JOIN cookies ON cookies.cookie_id = line_items.cookie_id
    WHERE users.username = %s
    2016-03-15 22:02:58,472 INFO sqlalchemy.engine.base.Engine ('cookiemon',)
    (1, 'cookiemon', '111-111-1111', 'chocolate chip', 2, Decimal('1.00'))
    (1, 'cookiemon', '111-111-1111', 'white chocolate chip and macadamia nut', 12, Decimal('3.00'))

    In [3]: run joins2.py
    2016-03-15 22:07:41,410 INFO sqlalchemy.engine.base.Engine SELECT users.username, count(orders.order_id) AS count_1
    FROM users LEFT OUTER JOIN orders ON users.user_id = orders.user_id GROUP BY users.username
    2016-03-15 22:07:41,410 INFO sqlalchemy.engine.base.Engine ()
    ('cakeeater', 1)
    ('cookiemon', 1)
    ('pieguy', 0)

SQLAlchemy knows how to join the `users` and `orders` tables because of the foreign
key defined in the `orders` table.

## Aliases

When using joins, we often need to refer to a table more than once. In SQL, we use
_aliases_ for this. Suppose we have the following (partial) schema for an org
chart:

    employee_table = Table(
        'employee', metadata,
        Column('id', Integer, primary_key=True),
        Column('manager', None, ForeignKey('employee.id')),
        Column('name', String(255)))

What if we want to select all employees managed by an employee named 'Fred'? In
SQL, we would write:

    SELECT employee.name
    FROM employee, employee AS manager
    WHERE employee.manager_id = manager.id
    AND manager.name = 'Fred';

SQLAlchemy also offers an `alias()`.

    In [1]: run alias1.py
    SELECT employee.name
    FROM employee, employee AS mgr
    WHERE employee.manager_id = mgr.id AND mgr.name = :name_1

SQLAlchemy may also select the name automatically, which is useful for avoiding
collisions.

## Grouping

When grouping, we need one or more columns to group on and one or more columns
that is makes sense to aggregate with counts, sums, etc.

    In [1]: run grouping1.py
    2016-03-18 19:18:31,211 INFO sqlalchemy.engine.base.Engine SHOW VARIABLES LIKE 'sql_mode'
    ...
    2016-03-18 19:18:31,237 INFO sqlalchemy.engine.base.Engine SELECT users.username, count(orders.order_id) AS count_1
    FROM users LEFT OUTER JOIN orders ON users.user_id = orders.user_id GROUP BY users.username
    2016-03-18 19:18:31,237 INFO sqlalchemy.engine.base.Engine ()
    ('cakeeater', 1)
    ('cookiemon', 1)
    ('pieguy', 0)
    
## Chaining

Chaining is particularly useful when we're applying logic to build up a query.

    In [2]: run chaining1.py
    2016-03-18 19:54:14,948 INFO sqlalchemy.engine.base.Engine SELECT orders.order_id, users.username, users.phone, cookies.cookie_name, line_items.quantity, line_items.extended_cost
    FROM users INNER JOIN orders ON users.user_id = orders.user_id INNER JOIN line_items ON orders.order_id = line_items.order_id INNER JOIN cookies ON cookies.cookie_id = line_items.cookie_id
    WHERE users.username = %s
    2016-03-18 19:54:14,948 INFO sqlalchemy.engine.base.Engine ('cakeeater',)
    (2, 'cakeeater', '222-222-2222', 'chocolate chip', 24, Decimal('12.00'))
    (2, 'cakeeater', '222-222-2222', 'peanut butter', 6, Decimal('6.00'))
    
