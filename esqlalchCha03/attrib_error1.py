#!/usr/bin/env python
from __future__ import print_function

from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import exc

import cookies_tables
connection = cookies_tables.engine.connect()

print('\nAttempting to violate unique key...\n')

ins = insert(cookies_tables.users).values(
    username='bruleboy',
    email_address='bb@desert.org',
    phone='222-123-4444',
    password='firetruck!4evar'
)
try:
    print("\nExecuting insert...\n")
    retult = connection.execute(ins)
    print("\nInsert finished.\n")
except exc.IntegrityError as e:
    print("\nException message:\n")
    print(e)

print("\nLet's look in the db...\n")

s = select([
    cookies_tables.users.c.username,
    cookies_tables.users.c.password
])
results = connection.execute(s)
for result in results:
    print('{:>20} : {:>20}'.format(result.username, result.password))
