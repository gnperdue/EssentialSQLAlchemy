from sqlalchemy import MetaData
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer, Numeric, Boolean, String
# from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy import CheckConstraint
from sqlalchemy import create_engine

from datetime import datetime
from sqlalchemy import DateTime

from mariadb_connect import conn_str

metadata = MetaData()

cookies = Table('cookies', metadata,
                Column('cookie_id', Integer(), primary_key=True),
                Column('cookie_name', String(50), index=True),
                Column('cookie_recipe_url', String(255)),
                Column('cookie_sku', String(55)),
                Column('quantity', Integer()),
                Column('unit_cost', Numeric(12, 2)),
                CheckConstraint('unit_cost >= 0.00',
                                name='unit_cost_positive'),
                CheckConstraint('quantity >= 0.00',
                                name='quantity_positive')
                )

# Instead of specifying the index inside the `Column`, we could say:
# from sqlalchemy import Index
# Index('ix_cookies_cookie_name', 'cookie_name')

# note that we set the `default` and `onupdate` times equal to the callable
# function instead of calling the function - this means we get the time
# the records themselves are actually created or updated.
users = Table('users', metadata,
              Column('user_id', Integer(), primary_key=True),
              Column('username', String(15), nullable=False, unique=True),
              Column('email_address', String(255), nullable=False),
              Column('phone', String(20), nullable=False),
              Column('password', String(25), nullable=False),
              Column('created_on', DateTime(), default=datetime.now),
              Column('updated_on', DateTime(), default=datetime.now,
                     onupdate=datetime.now))

# Instead of specifying these in the `Column` declaration, we can say:
# PrimaryKeyConstraint('user_id', name='user_pk')
# UniqueConstraint('username', name='uix_username')

# Note that we use strings instead of references to actual tables when creating
# the `ForeignKey`: this allows us to separate table definitions across
# multiple modules and to not worry about the order in which tables are loaded.
orders = Table('orders', metadata,
               Column('order_id', Integer(), primary_key=True),
               Column('user_id', ForeignKey('users.user_id')),
               Column('shipped', Boolean(), default=False))

line_items = Table('line_items', metadata,
                   Column('line_items_id', Integer(), primary_key=True),
                   Column('order_id', ForeignKey('orders.order_id')),
                   Column('cookie_id', ForeignKey('cookies.cookie_id')),
                   Column('quantity', Integer()),
                   Column('extended_cost', Numeric(12, 2)))

# Instead of defining the `ForeignKey` in the `Column`, we could have said,
# from sqlalchemy import ForeignKeyConstraint
# ForeignKeyConstraint(['order_id'], ['orders.order_id'])
# This creates a constraint for the `order_id` field between the `line_items`
# table and the `orders` table.

engine = create_engine(conn_str, echo=True)

# Okay to keep the `create_all` around indefinitely - in fact, it seems
# SQLAlchemy doesn't event really create the "basic connection" without this...
metadata.create_all(engine)
