from __future__ import print_function

from sqlalchemy import select
from sqlalchemy import desc

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

s = select([cookies_tables.cookies.c.cookie_name,
            cookies_tables.cookies.c.quantity])
s = s.order_by(desc(cookies_tables.cookies.c.quantity))
rp = connection.execute(s)
for cookie in rp:
    print('{} - {}'.format(cookie.quantity, cookie.cookie_name))
