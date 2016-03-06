from __future__ import print_function

from sqlalchemy import select
from sqlalchemy import or_
# from sqlalchemy import and_, not_

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

s = select([cookies_tables.cookies]).where(
    or_(cookies_tables.cookies.c.quantity.between(10, 50),
        cookies_tables.cookies.c.cookie_name.contains('chip'))
)
for row in connection.execute(s):
    print(row.cookie_name)
