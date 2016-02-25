import model
from sqlalchemy import orm
from sqlalchemy import create_engine

from mariadb_connect import db_conn_str

# create an engine and create all the tables we need
engine = create_engine(db_conn_str('tester'), echo=True)
model.metadata.bind = engine
model.metadata.create_all()

# set up the session
# `sessionmaker` returns an object for building the session we want
# * `flushing` is the process of updating the db with the objects we're using
# * `commiting` is sending a `COMMIT` statement to the db to make flushes
# permanent
#
# `bind=engine` - bind the session to the engine; the session will create the
# connection it needs
# `autoflush=True` - if we comit changes to the db before they have been
# flushed, this option will tell SQLAlchemy to flush them before the commit
# is gone
# `autocommit=False` - wrap all changes between commits in a transation; if
# `True`, this will cause SQLAlchemy to commit any changes after each flush
# (usually we don't want this)
# `expire_on_commit=True` - all instances attached to the session will be
# expired after each commit so all access subsequent to a completed transaction
# will load from the most recent db state
sm = orm.sessionmaker(bind=engine,
                      autoflush=True,
                      autocommit=False,
                      expire_on_commit=True)
# the `scoped_session()` object makes sure a different session is used for
# each thread so every request has its own access to the db
session = orm.scoped_session(sm)
