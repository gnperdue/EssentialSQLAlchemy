from __future__ import print_function

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

ins = cookies_tables.cookies.insert()
result = connection.execute(
    ins,
    cookie_name="dark chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe_dark.html",
    cookie_sku="CC02",
    quantity="1",
    unit_cost="0.75")
result.inserted_primary_key
