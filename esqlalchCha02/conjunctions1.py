from __future__ import print_function

from sqlalchemy import select
from sqlalchemy import and_
# from sqlalchemy import or_, not_

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

s = select([cookies_tables.cookies]).where(
    and_(cookies_tables.cookies.c.quantity > 23,
         cookies_tables.cookies.c.unit_cost < 0.40)
)
for row in connection.execute(s):
    print(row.cookie_name)
