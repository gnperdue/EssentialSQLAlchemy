from __future__ import print_function

from sqlalchemy import select

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()


def get_orders_by_customer(cust_name, shipped=None, details=False):
    columns = [cookies_tables.orders.c.order_id,
               cookies_tables.users.c.username,
               cookies_tables.users.c.phone,
    ]
    joins = cookies_tables.users.join(cookies_tables.orders)
    if details:
        columns.extend([cookies_tables.cookies.c.cookie_name,
                        cookies_tables.line_items.c.quantity,
                        cookies_tables.line_items.c.extended_cost,
                        ])
        joins = joins.join(
            cookies_tables.line_items).join(
                cookies_tables.cookies)
    cust_orders = select(columns)
    cust_orders = cust_orders.select_from(joins)
    cust_orders = cust_orders.where(
        cookies_tables.users.c.username == cust_name)
    if shipped is not None:
        cust_orders = cust_orders.where(
            cookies_tables.orders.c.shipped == shipped)
    result = connection.execute(cust_orders).fetchall()
    return result

res = get_orders_by_customer('cakeeater')
for row in res:
    print(row)

res = get_orders_by_customer('cakeeater', details=True)
for row in res:
    print(row)

res = get_orders_by_customer('cakeeater', shipped=True)
for row in res:
    print(row)

res = get_orders_by_customer('cakeeater', shipped=False)
for row in res:
    print(row)

res = get_orders_by_customer('cakeeater', shipped=False, details=True)
for row in res:
    print(row)
