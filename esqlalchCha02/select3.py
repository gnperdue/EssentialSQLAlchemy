from __future__ import print_function

from sqlalchemy import select

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

s = select([cookies_tables.cookies.c.cookie_name,
            cookies_tables.cookies.c.quantity])
rp = connection.execute(s)
print(rp.keys())
result = rp.first()
print(result)
