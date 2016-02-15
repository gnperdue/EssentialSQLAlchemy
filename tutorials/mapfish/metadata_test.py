from sqlalchemy import schema, types

metadata = schema.MetaData()

page_table = schema.Table(
    'page', metadata,
    schema.Column('id', types.Integer, primary_key=True),
    schema.Column('name', types.Unicode(255), default=u''),
    schema.Column('title', types.Unicode(255), default=u'Untitled Page'),
    schema.Column('content', types.Text(), default=u'')
)
