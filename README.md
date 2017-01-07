These are my personal notes for **Essential SQLAlchemy** by J. Meyers and R. 
Copeland, from O'Reilly books.

## Working with the dbs

First, source `setup.sh` to get `$PYTHONPATH` configured to use the db access
code.

## First time set up

We assume the database `essential_alchemy` exists with no tables. If needed,
create the db or `DROP TABLE`, etc. 

    MariaDB [(none)]> CREATE DATABASE essential_alchemy;
    MariaDB [(none)]> SHOW DATABASES;
    MariaDB [(none)]> USE essential_alchemy;
    MariaDB [essential_alchemy]> SHOW TABLES;

Then, with `$PYTHONPATH` configured correctly,

    EssentialSQLAlchemy$ python cookies_tables.py

This will create the set of empty tables:

    MariaDB [essential_alchemy]> SHOW TABLES;
    +-----------------------------+
    | Tables_in_essential_alchemy |
    +-----------------------------+
    | cookies                     |
    | line_items                  |
    | orders                      |
    | users                       |
    +-----------------------------+
    4 rows in set (0.00 sec)

The structure of the db evolves are we move through the book and is basically
always in the "most advanced" state, so some parts of the table structure
created may not be exactly what is in the book in early chapters, etc.
