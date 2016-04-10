from __future__ import print_function

from sqlalchemy import insert

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

# cookies
ins = cookies_tables.cookies.insert()
inventory_list = [
    {
        'cookie_name': 'chocolate chip',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/chochip.html',
        'cookie_sku': 'CC01',
        'quantity': '12',
        'unit_cost': '0.50'
    },
    {
        'cookie_name': 'dark chocolate chip',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/dark.html',
        'cookie_sku': 'CC02',
        'quantity': '1',
        'unit_cost': '0.75'
    },
    {
        'cookie_name': 'white chocolate chip and macadamia nut',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/whit_cho_mac.html',
        'cookie_sku': 'CC03',
        'quantity': '1',
        'unit_cost': '1.00'
    },
    {
        'cookie_name': 'peanut butter',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/peanut.html',
        'cookie_sku': 'PB01',
        'quantity': '24',
        'unit_cost': '0.25'
    },
    {
        'cookie_name': 'oatmeal raisin',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/raisin.html',
        'cookie_sku': 'EWW01',
        'quantity': '100',
        'unit_cost': '1.00'
    }
]
result = connection.execute(
    ins,
    inventory_list
)

# customers
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

# order + line_item together...
ins = insert(cookies_tables.orders).values(user_id=1, order_id=1)
result = connection.execute(ins)
ins = insert(cookies_tables.line_items)
order_items = [
    {
        'order_id': 1,
        'cookie_id': 1,
        'quantity': 9,
        'extended_cost': 4.50
    }
]
result = connection.execute(ins, order_items)

# order + line_item together...
ins = insert(cookies_tables.orders).values(user_id=1, order_id=2)
result = connection.execute(ins)
ins = insert(cookies_tables.line_items)
order_items = [
    {
        'order_id': 2,
        'cookie_id': 1,
        'quantity': 4,
        'extended_cost': 1.50
    },
    {
        'order_id': 2,
        'cookie_id': 2,
        'quantity': 1,
        'extended_cost': 4.50
    },
]
result = connection.execute(ins, order_items)
