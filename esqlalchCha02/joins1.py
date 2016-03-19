from __future__ import print_function

from sqlalchemy import select

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

columns = [cookies_tables.orders.c.order_id, cookies_tables.users.c.username,
           cookies_tables.users.c.phone, cookies_tables.cookies.c.cookie_name,
           cookies_tables.line_items.c.quantity,
           cookies_tables.line_items.c.extended_cost]

cookimon_orders = select(columns)
cookimon_orders = cookimon_orders.select_from(
    cookies_tables.orders.join(
        cookies_tables.users).join(
            cookies_tables.line_items).join(
                cookies_tables.cookies)).where(
                    cookies_tables.users.c.username == 'cookiemon')

result = connection.execute(cookimon_orders).fetchall()
for row in result:
    print(row)
