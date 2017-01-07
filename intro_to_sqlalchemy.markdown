# Intro

## Why Use SQLAlchemy?

Abstract code away from the underlying database and its SQL particulars. It also
ensures proper sanitization and escaping to mitigate SQL-injection attacks. It
offers both "Core" and "ORM" (object-relational mapper) methods of working.

## Choosing Between Core and ORM

Core has a schema-centric view focused around tables, keys, and index structures.
The ORM focuses more on domain-driven design.

## Installing SQLAlchemy and Connecting to a Database

Basic SQLAlchemy comes with Anaconda.

### Installing Database Drivers

* PostgreSQL
* MySQL
* Others

Running with Python 2.7:

    EssentialSQLAlchemy$ ipython
    Python 2.7.11 |Anaconda 2.4.1 (x86_64)| (default, Dec  6 2015, 18:57:58)
    Type "copyright", "credits" or "license" for more information.
    
    IPython 4.0.1 -- An enhanced Interactive Python.
    ?         -> Introduction and overview of IPython's features.
    %quickref -> Quick reference.
    help      -> Python's own help system.
    object?   -> Details about 'object', use 'object??' for extra details.
    
    In [1]: import sqlalchemy
    
    In [2]: import pymysql
    
    In [3]:

Installed via `conda`:

    EssentialSQLAlchemy$ conda list | grep sql
    pymysql                   0.7.9                    py27_0
    sqlalchemy                1.0.12                   py27_0
    sqlite                    3.13.0                        0

### Connecting to a Database

We connect to a db via an _engine_. SQLite:

    In [1]: from sqlalchemy import create_engine
    
    In [2]: engine = create_engine('sqlite:///cookies.db')
    
    In [3]: import os
    
    In [4]: loc = os.environ['HOME'] + \
       ...: '/Dropbox/Programming/Programming/Python/EssentialSQLAlchemy/'
    
    In [5]: engine2 = create_engine('sqlite://' + loc + 'cookies2.db')

Attempting to use MariaDB... Start the server:

    SQL$ mysql.server start
    Starting MySQL
    . SUCCESS!

Test login:

    SQL$ mysql -u gnperdue -p
    Enter password:
    Welcome to the MariaDB monitor.  Commands end with ; or \g.
    Your MariaDB connection id is 7
    Server version: 10.0.18-MariaDB Homebrew
    
    Copyright (c) 2000, 2015, Oracle, MariaDB Corporation Ab and others.
    
    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
    
    MariaDB [(none)]> Bye

And in Python...

    In [11]: conn_str = 'mysql+pymysql://' + username + ':' + passwd + \
       ....: '@localhost/library'
    
    In [12]: engine_mdb = create_engine(conn_str)
    
    In [13]: connection = engine_mdb.connect()

Working?...

    In [5]: conn_str = 'mysql+pymysql://' + username + ':' + passwd + \
       ...: '@localhost/db_does_not_exist'
    
    In [6]: engine = create_engine(conn_str)
    
    In [7]: connection = engine.connect()
    ---------------------------------------------------------------------------
    InternalError                             Traceback (most recent call last)
    ...
    
    InternalError: (pymysql.err.InternalError) (1049, u"Unknown database 'db_does_not_exist'")

Okay, so it probably does work when we use an existing `DATABASE`.

