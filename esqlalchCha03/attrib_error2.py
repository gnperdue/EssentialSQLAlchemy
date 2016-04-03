#!/usr/bin/env python
from __future__ import print_function

from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

import cookies_tables
connection = cookies_tables.engine.connect()

ins = insert(cookies_tables.users).values(
    username='bruleboy',
    email_address='bb@desert.org',
    phone='222-123-4444',
    password='firetruck!4evar'
)
try:
    retult = connection.execute(ins)
except IntegrityError as error:
    print(error)

s = select([cookies_tables.users.c.username])
results = connection.execute(s)
for result in results:
    print(result.username)
    print(result.password)
