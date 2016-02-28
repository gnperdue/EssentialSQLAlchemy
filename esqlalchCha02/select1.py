from __future__ import print_function

from sqlalchemy import select

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

s = select([cookies_tables.cookies])
rp = connection.execute(s)
results = rp.fetchall()
print(results)
