from __future__ import print_function

from sqlalchemy import select
from sqlalchemy import update

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()


def ship_it(order_id):
    s = select([cookies_tables.line_items.c.cookie_id,
                cookies_tables.line_items.c.quantity])
    s = s.where(cookies_tables.line_items.c.order_id == order_id)
    cookies_to_ship = connection.execute(s)
    for cookie in cookies_to_ship:
        u = update(cookies_tables.cookies).where(
            cookies_tables.cookies.c.cookie_id == cookie.cookie_id
        )
        u = u.values(
            quantity=cookies_tables.cookies.c.quantity - cookie.quantity
        )
        result = connection.execute(u)
    u = update(cookies_tables.orders).where(
        cookies_tables.orders.c.order_id == order_id
    )
    u = u.values(shipped=True)
    result = connection.execute(u)
    print("Shipped order id: {}".format(order_id))

print("Check before shipping...\n")
s = select([cookies_tables.cookies.c.cookie_name,
            cookies_tables.cookies.c.quantity])
result = connection.execute(s).fetchall()
for row in result:
    print(row)

# comment this out in case we accidently run this, but it should be in for
# following along with the text...
# print("Shipping order...\n")
# ship_it(1)

print("Check after shipping...\n")
s = select([cookies_tables.cookies.c.cookie_name,
            cookies_tables.cookies.c.quantity])
result = connection.execute(s).fetchall()
for row in result:
    print(row)

