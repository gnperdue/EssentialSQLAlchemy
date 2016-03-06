from __future__ import print_function

from sqlalchemy import select
from sqlalchemy import func

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

s = select([
    func.count(cookies_tables.cookies.c.cookie_name).label('inventory_count')
])
rp = connection.execute(s)
record = rp.first()
print(record.keys())
print(record.inventory_count)
