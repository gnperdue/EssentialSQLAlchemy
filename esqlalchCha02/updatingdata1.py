from __future__ import print_function

from sqlalchemy import select
from sqlalchemy import update

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

u = update(cookies_tables.cookies).where(
    cookies_tables.cookies.c.cookie_name == 'chocolate chip'
)
u = u.values(quantity=(cookies_tables.cookies.c.quantity + 120))
result = connection.execute(u)
print(result.rowcount)
s = select([cookies_tables.cookies]).where(
    cookies_tables.cookies.c.cookie_name == 'chocolate chip'
)
result = connection.execute(s).first()
for key in result.keys():
    print('{:>20}: {}'.format(key, result[key]))
