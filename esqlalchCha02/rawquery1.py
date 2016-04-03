from __future__ import print_function

from sqlalchemy import select
from sqlalchemy import text

# bring in the table defs
import cookies_tables

# connect to our db
connection = cookies_tables.engine.connect()

stmt = select([cookies_tables.users]).where(text("username='cookiemon'"))
print(connection.execute(stmt).fetchall())
