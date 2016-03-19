from __future__ import print_function

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import MetaData
from sqlalchemy import ForeignKey

from sqlalchemy import select
from sqlalchemy import and_


metadata = MetaData()

employee_table = Table(
    'employee', metadata,
    Column('id', Integer(), primary_key=True),
    Column('manager_id', Integer(), ForeignKey('employee.id')),
    Column('name', String(255))
)

manager = employee_table.alias('mgr')
stmt = select([employee_table.c.name],
              and_(employee_table.c.manager_id == manager.c.id,
                   manager.c.name == 'Fred'))
print(stmt)
