from __future__ import print_function

from sqlalchemy import insert

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

customer_list = [
    {
        'username': 'cookiemon',
        'email_address': 'mon@cookie.com',
        'phone': '111-111-1111',
        'password': 'password',
    },
    {
        'username': 'cakeeater',
        'email_address': 'cakeeater@cake.com',
        'phone': '222-222-2222',
        'password': 'password1',
    },
    {
        'username': 'pieguy',
        'email_address': 'guy@pie.com',
        'phone': '333-333-3333',
        'password': 'password2',
    },
]
ins = cookies_tables.users.insert()
result = connection.execute(ins, customer_list)

ins = insert(cookies_tables.orders).values(user_id=1, order_id=1)
result = connection.execute(ins)

ins = insert(cookies_tables.line_items)
order_items = [
    {
        'order_id': 1,
        'cookie_id': 1,
        'quantity': 2,
        'extended_cost': 1.00
    },
    {
        'order_id': 1,
        'cookie_id': 2,
        'quantity': 12,
        'extended_cost': 3.00
    },
]
result = connection.execute(ins, order_items)

ins = insert(cookies_tables.orders).values(user_id=2, order_id=2)
result = connection.execute(ins)

ins = insert(cookies_tables.line_items)
order_items = [
    {
        'order_id': 2,
        'cookie_id': 1,
        'quantity': 24,
        'extended_cost': 12.00
    },
    {
        'order_id': 2,
        'cookie_id': 4,
        'quantity': 6,
        'extended_cost': 6.00
    },
]
result = connection.execute(ins, order_items)
