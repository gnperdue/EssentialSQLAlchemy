from __future__ import print_function

from sqlalchemy import select
from sqlalchemy import func

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

columns = [cookies_tables.users.c.username,
           func.count(cookies_tables.orders.c.order_id)]

all_orders = select(columns)
all_orders = all_orders.select_from(
    cookies_tables.users.outerjoin(cookies_tables.orders))
all_orders = all_orders.group_by(cookies_tables.users.c.username)

result = connection.execute(all_orders).fetchall()
for row in result:
    print(row)
