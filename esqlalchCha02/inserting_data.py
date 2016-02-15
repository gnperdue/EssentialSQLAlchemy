from __future__ import print_function
from sqlalchemy import create_engine
from sqlalchemy import insert

from mariadb_connect import conn_str


engine_mdb = create_engine(conn_str)
connection = engine_mdb.connect()

ins = cookies.insert().values(
    cookie_name="chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
    cookie_sku="CC01",
    quantity="12",
    unit_cost="0.50")
print(str(ins))
