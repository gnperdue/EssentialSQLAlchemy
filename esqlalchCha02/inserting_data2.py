from __future__ import print_function
from sqlalchemy import insert

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

ins = insert(cookies_tables.cookies).values(
    cookie_name="white chocolate chip and macadamia nut",
    cookie_recipe_url="http://some.aweso.me/cookie/white_choc_maca_nut.html",
    cookie_sku="CC03",
    quantity="1",
    unit_cost="1.00")

result = connection.execute(ins)
