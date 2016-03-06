from __future__ import print_function

from sqlalchemy import select
from sqlalchemy import func

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

s = select([func.sum(cookies_tables.cookies.c.quantity)])
rp = connection.execute(s)
# return only the leftmost column in the first record with `scalar()`
print(rp.scalar())

s = select([cookies_tables.cookies.c.quantity])
rp = connection.execute(s)
sum = 0
for cookie in rp:
    sum += cookie.quantity
print(sum)

