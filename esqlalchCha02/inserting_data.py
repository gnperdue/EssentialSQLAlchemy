from __future__ import print_function
from sqlalchemy import insert

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

ins = cookies_tables.cookies.insert().values(
    cookie_name="chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
    cookie_sku="CC01",
    quantity="12",
    unit_cost="0.50")
print(str(ins))

result = connection.execute(ins)
