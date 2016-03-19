from __future__ import print_function

from sqlalchemy import select
from sqlalchemy import delete

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

u = delete(cookies_tables.cookies).where(
    cookies_tables.cookies.c.cookie_name == 'dark chocolate chip'
)
result = connection.execute(u)
print(result.rowcount)

s = select([cookies_tables.cookies]).where(
    cookies_tables.cookies.c.cookie_name == 'dark chocolate chip'
)
result = connection.execute(s).fetchall()
print(len(result))
