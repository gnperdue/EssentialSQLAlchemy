from __future__ import print_function

from sqlalchemy import select
from sqlalchemy import cast
from sqlalchemy import Numeric

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

s = select([
    cookies_tables.cookies.c.cookie_name,
    cast((cookies_tables.cookies.c.quantity *
          cookies_tables.cookies.c.unit_cost),
         Numeric(12, 2)).label('inv_cost')
    ])
for row in connection.execute(s):
    print('{} - {}'.format(row.cookie_name, row.inv_cost))
