from metadata_test import engine, page_table

connection = engine.connect()
ins = page_table.insert(
    values=dict(name=u'another test',
                title=u'A new page',
                content=u'Some hot content')
)
print ins
result = connection.execute(ins)
print result

connection.close()
