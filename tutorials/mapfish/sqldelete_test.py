from metadata_test import engine, page_table
from sqlalchemy.sql import delete

connection = engine.connect()

# pick out the row we will delete - use the id
d = delete(page_table, page_table.c.id == 1)
connection.execute(d)

