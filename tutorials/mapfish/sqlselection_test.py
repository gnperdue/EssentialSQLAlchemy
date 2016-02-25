from metadata_test import engine, page_table
from sqlalchemy.sql import select
from sqlalchemy.sql import and_
# from sqlalchemy.sql or_, not_

connection = engine.connect()

s = select([page_table])
result = connection.execute(s)
for row in result:
    print row

s = select([page_table],
           and_(page_table.c.id <= 10,
                page_table.c.name.like(u't%')))
s = s.order_by(page_table.c.title.desc(), page_table.c.id)
result = connection.execute(s)
print result.fetchall()
