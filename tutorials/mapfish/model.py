from sqlalchemy import orm
import datetime
from sqlalchemy import schema, types

metadata = schema.MetaData()


def now():
    return datetime.datetime.now()


page_table = schema.Table(
    'page', metadata,
    schema.Column('id',
                  types.Integer(),
                  schema.Sequence('page_seq_id', optional=True),
                  primary_key=True),
    schema.Column('content',
                  types.Text(),
                  nullable=False),
    schema.Column('posted',
                  types.DateTime(),
                  default=now),
    schema.Column('title',
                  types.Unicode(255),
                  default=u'Unititled Page'),
    schema.Column('heading',
                  types.Unicode(255)),
)

comment_table = schema.Table(
    'comment', metadata,
    schema.Column('id',
                  types.Integer(),
                  schema.Sequence('page_seq_id', optional=True),
                  primary_key=True),
    schema.Column('pageid',
                  types.Integer(),
                  schema.ForeignKey('page.id'),
                  nullable=False),
    schema.Column('content',
                  types.Text(),
                  default=u''),
    schema.Column('name',
                  types.Unicode(255)),
    schema.Column('email',
                  types.Unicode(255),
                  nullable=False),
    schema.Column('created',
                  types.TIMESTAMP(),
                  default=now),
)

pagetag_table = schema.Table(
    'pagetag', metadata,
    schema.Column('id',
                  types.Integer(),
                  schema.Sequence('pagetag_seq_id', optional=True),
                  primary_key=True),
    schema.Column('pageid',
                  types.Integer(),
                  schema.ForeignKey('page.id')),
    schema.Column('tagid',
                  types.Integer(),
                  schema.ForeignKey('tag.id')),
)

tag_table = schema.Table(
    'tag', metadata,
    schema.Column('id',
                  types.Integer(),
                  schema.Sequence('tag_seq_id', optional=True),
                  primary_key=True),
    schema.Column('name',
                  types.Unicode(20),
                  nullable=False,
                  unique=True),
)


class Page(object):
    pass


class Comment(object):
    pass


class Tag(object):
    pass


# `Page` class is mapped to `page_table`
# Tell SQLAlchemy that a `Page` object should have extra properties called
# `comments` and `tags` which should return all the `Comment` and `Tag` objects
# related to the page.
orm.mapper(Page, page_table, properties={
    'comments': orm.relation(Comment, backref='page'),
    'tags': orm.relation(Tag, secondary=pagetag_table)
    })

# `Comment` class is mapped to `comment_table`
# The mapper for `Comment` does not need a `page` property because the mapper
# for `Page` has already specified it via `backref`.
orm.mapper(Comment, comment_table)

# `Tag` class is mapped to `tag_table`
# The mapper for `Tag` does not need its relation to `Page` specified because
# SQLALchemy can deduce it from the `secondary` argument.
orm.mapper(Tag, tag_table)
