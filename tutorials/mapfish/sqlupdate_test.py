from metadata_test import engine, page_table
from sqlalchemy.sql import update

connection = engine.connect()

# pick out the row we will update - look for a match with title == 'Test page'
u = update(page_table, page_table.c.title == u'Test page')
connection.execute(u, title=u"Updated Title")
