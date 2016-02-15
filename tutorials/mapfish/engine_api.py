from __future__ import print_function
from sqlalchemy.engine import create_engine

from mariadb_connect import db_conn_str

# `echo=True` => log all SQL to stdout
engine = create_engine(db_conn_str('tester'), echo=True)
connection = engine.connect()

connection.execute(
"""
CREATE TABLE users (
username VARCHAR(32) PRIMARY KEY,
password VARCHAR(128) NOT NULL
);
"""
)

connection.execute(
    "INSERT INTO users (username, password) VALUES (\"%s\", \"%s\");" %
    ("foo", "bar")
)

# `result` is a `ResultProxy`
result = connection.execute("SELECT username FROM users")
for row in result:
    print("username:", row['username'])
    
connection.close()
