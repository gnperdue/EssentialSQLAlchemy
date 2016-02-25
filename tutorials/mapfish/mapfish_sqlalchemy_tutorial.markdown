# SQLAlchemy tutorial

Following (sort of): http://mapfish.org/doc/tutorials/sqlalchemy.html

## Installing

...

## Engine API

... see `engine_api.py`

## Metadata and Type APIs

The metadata and type systems combine to describe the database schema in
an RDBMS-independent manner.

The `metadata` object holds all the information about the tables, columns, types,
foreign keys, indexes, etc. that make up the DB structure. It may be used to
create tables - bind it to an engine and call `create_all()`.

## SQL Expression API

### Inserting

SQLAlchemy handles type conversion for values in `insert()` commands, removng
the possibility of SQL injection attacks.

### Selecting

To add `WHERE` clauses, pass a SQLAlchemy expression as the second argument to the
`select()` call.

### Updating

Use `update()` to update tables.

### Deleting

Use `delete()` to delete entries.

## Object-Relational API

The highest-levle API SQLAlchemy provides is the Object-Relational API. It works
directly with objects and avoids much of the particulars of SQL. See `model.py`.

* we use `primary_key=True` to tell SQLAlchemy about primary keys
* we use `ForeignKey` to tell how tables are related
* we use `Sequence`
* we use `unique=True` to enforce `UNIQUE` constraints

### Mapping

With the table scructure defined, we need to define classes and mappers to
work with the Object-Relational API. See `model.py`.

### Create the Session

SQLAlchemy manages the mapped objects inside a "session." See `object_test.py`.

### Use the Session

We may use the session to insert, delete, update, and query the db, etc.

#### Insert

    In [2]: from object_test import session
    2016-02-21 18:01:33,419 INFO sqlalchemy.engine.base.Engine SHOW VARIABLES LIKE 'sql_mode'
    2016-02-21 18:01:33,420 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:01:33,424 INFO sqlalchemy.engine.base.Engine SELECT DATABASE()
    2016-02-21 18:01:33,424 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:01:33,425 INFO sqlalchemy.engine.base.Engine show collation where `Charset` = 'utf8' and `Collation` = 'utf8_bin'
    2016-02-21 18:01:33,426 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:01:33,435 INFO sqlalchemy.engine.base.Engine SELECT CAST('test plain returns' AS CHAR(60)) AS anon_1
    2016-02-21 18:01:33,435 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:01:33,439 INFO sqlalchemy.engine.base.Engine SELECT CAST('test unicode returns' AS CHAR(60)) AS anon_1
    2016-02-21 18:01:33,440 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:01:33,441 INFO sqlalchemy.engine.base.Engine SELECT CAST('test collated returns' AS CHAR CHARACTER SET utf8) COLLATE utf8_bin AS anon_1
    2016-02-21 18:01:33,441 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:01:33,445 INFO sqlalchemy.engine.base.Engine DESCRIBE `comment`
    2016-02-21 18:01:33,445 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:01:33,452 INFO sqlalchemy.engine.base.Engine ROLLBACK
    2016-02-21 18:01:33,453 INFO sqlalchemy.engine.base.Engine DESCRIBE `tag`
    2016-02-21 18:01:33,453 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:01:33,456 INFO sqlalchemy.engine.base.Engine ROLLBACK
    2016-02-21 18:01:33,457 INFO sqlalchemy.engine.base.Engine DESCRIBE `pagetag`
    2016-02-21 18:01:33,457 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:01:33,460 INFO sqlalchemy.engine.base.Engine ROLLBACK
    2016-02-21 18:01:33,460 INFO sqlalchemy.engine.base.Engine DESCRIBE `page`
    2016-02-21 18:01:33,461 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:01:33,466 INFO sqlalchemy.engine.base.Engine
    CREATE TABLE comment (
    id INTEGER NOT NULL AUTO_INCREMENT,
    pageid INTEGER NOT NULL,
    content TEXT,
    name VARCHAR(255),
    email VARCHAR(255) NOT NULL,
    created TIMESTAMP NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(pageid) REFERENCES page (id)
    )
    
    
    2016-02-21 18:01:33,467 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:01:33,725 INFO sqlalchemy.engine.base.Engine COMMIT
    2016-02-21 18:01:33,727 INFO sqlalchemy.engine.base.Engine
    CREATE TABLE tag (
    id INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (name)
    )
    
    
    2016-02-21 18:01:33,727 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:01:33,752 INFO sqlalchemy.engine.base.Engine COMMIT
    2016-02-21 18:01:33,754 INFO sqlalchemy.engine.base.Engine
    CREATE TABLE pagetag (
    id INTEGER NOT NULL AUTO_INCREMENT,
    pageid INTEGER,
    tagid INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(pageid) REFERENCES page (id),
    FOREIGN KEY(tagid) REFERENCES tag (id)
    )
    
    
    2016-02-21 18:01:33,755 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:01:33,780 INFO sqlalchemy.engine.base.Engine COMMIT

Then...

    In [3]: import model
    
    In [4]: test_page = model.Page()
    
    In [5]: test_page.title = u'Test Page'
    
    In [6]: test_page.content = u'Test content'
    
    In [8]: test_page.title
    Out[8]: u'Test Page'
    
    In [9]: session.add(test_page)
    
    In [10]: print test_page.id
    None
    
    In [11]: session.flush()
    2016-02-21 18:04:20,319 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)
    2016-02-21 18:04:20,321 INFO sqlalchemy.engine.base.Engine INSERT INTO page (content, posted, title, heading) VALUES (%s, %s, %s, %s)
    2016-02-21 18:04:20,321 INFO sqlalchemy.engine.base.Engine (u'Test content', datetime.datetime(2016, 2, 21, 18, 4, 20, 321075), u'Test Page', None)
    2016-02-21 18:04:20,323 INFO sqlalchemy.engine.base.Engine ROLLBACK
    ...

    InternalError: (pymysql.err.InternalError) (1054, u"Unknown column 'posted' in 'field list'") [SQL: u'INSERT INTO page (content, posted, title, heading) VALUES (%s, %s, %s, %s)'] [parameters: (u'Test content', datetime.datetime(2016, 2, 21, 18, 4, 20, 321075), u'Test Page', None)]

Problem was an old version of the `page` table already existed. Blow it all away
and try again...

    In [1]: from object_test import session
    2016-02-21 18:10:11,162 INFO sqlalchemy.engine.base.Engine SHOW VARIABLES LIKE 'sql_mode'
    2016-02-21 18:10:11,162 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:10:11,164 INFO sqlalchemy.engine.base.Engine SELECT DATABASE()
    2016-02-21 18:10:11,164 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:10:11,165 INFO sqlalchemy.engine.base.Engine show collation where `Charset` = 'utf8' and `Collation` = 'utf8_bin'
    2016-02-21 18:10:11,165 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:10:11,167 INFO sqlalchemy.engine.base.Engine SELECT CAST('test plain returns' AS CHAR(60)) AS anon_1
    2016-02-21 18:10:11,167 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:10:11,168 INFO sqlalchemy.engine.base.Engine SELECT CAST('test unicode returns' AS CHAR(60)) AS anon_1
    2016-02-21 18:10:11,168 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:10:11,169 INFO sqlalchemy.engine.base.Engine SELECT CAST('test collated returns' AS CHAR CHARACTER SET utf8) COLLATE utf8_bin AS anon_1
    2016-02-21 18:10:11,169 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:10:11,170 INFO sqlalchemy.engine.base.Engine DESCRIBE `comment`
    2016-02-21 18:10:11,170 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:10:11,173 INFO sqlalchemy.engine.base.Engine ROLLBACK
    2016-02-21 18:10:11,173 INFO sqlalchemy.engine.base.Engine DESCRIBE `tag`
    2016-02-21 18:10:11,173 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:10:11,174 INFO sqlalchemy.engine.base.Engine ROLLBACK
    2016-02-21 18:10:11,175 INFO sqlalchemy.engine.base.Engine DESCRIBE `pagetag`
    2016-02-21 18:10:11,175 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:10:11,176 INFO sqlalchemy.engine.base.Engine ROLLBACK
    2016-02-21 18:10:11,177 INFO sqlalchemy.engine.base.Engine DESCRIBE `page`
    2016-02-21 18:10:11,177 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:10:11,178 INFO sqlalchemy.engine.base.Engine ROLLBACK
    2016-02-21 18:10:11,180 INFO sqlalchemy.engine.base.Engine
    CREATE TABLE tag (
    id INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (name)
    )
    
    
    2016-02-21 18:10:11,180 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:10:11,224 INFO sqlalchemy.engine.base.Engine COMMIT
    2016-02-21 18:10:11,225 INFO sqlalchemy.engine.base.Engine
    CREATE TABLE page (
    id INTEGER NOT NULL AUTO_INCREMENT,
    content TEXT NOT NULL,
    posted DATETIME,
    title VARCHAR(255),
    heading VARCHAR(255),
    PRIMARY KEY (id)
    )
    
    
    2016-02-21 18:10:11,226 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:10:11,247 INFO sqlalchemy.engine.base.Engine COMMIT
    2016-02-21 18:10:11,249 INFO sqlalchemy.engine.base.Engine
    CREATE TABLE comment (
    id INTEGER NOT NULL AUTO_INCREMENT,
    pageid INTEGER NOT NULL,
    content TEXT,
    name VARCHAR(255),
    email VARCHAR(255) NOT NULL,
    created TIMESTAMP NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(pageid) REFERENCES page (id)
    )
    
    
    2016-02-21 18:10:11,249 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:10:11,265 INFO sqlalchemy.engine.base.Engine COMMIT
    2016-02-21 18:10:11,266 INFO sqlalchemy.engine.base.Engine
    CREATE TABLE pagetag (
    id INTEGER NOT NULL AUTO_INCREMENT,
    pageid INTEGER,
    tagid INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(pageid) REFERENCES page (id),
    FOREIGN KEY(tagid) REFERENCES tag (id)
    )
    
    
    2016-02-21 18:10:11,267 INFO sqlalchemy.engine.base.Engine ()
    2016-02-21 18:10:11,290 INFO sqlalchemy.engine.base.Engine COMMIT

And

    In [2]: import model
    
    In [3]: test_page = model.Page()
    
    In [4]: test_page.title = u'Test Page'
    
    In [5]: test_page.content = u'Test Content'
    
    In [6]: test_page.title
    Out[6]: u'Test Page'
    
    In [7]: session.add(test_page)
    
    In [8]: print test_page.id
    None
    
    In [9]: session.flush()
    2016-02-21 18:11:59,322 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)
    2016-02-21 18:11:59,325 INFO sqlalchemy.engine.base.Engine INSERT INTO page (content, posted, title, heading) VALUES (%s, %s, %s, %s)
    2016-02-21 18:11:59,325 INFO sqlalchemy.engine.base.Engine (u'Test Content', datetime.datetime(2016, 2, 21, 18, 11, 59, 325064), u'Test Page', None)
    
    In [10]: print test_page.id
    1
    
    In [11]: session.commit()
    2016-02-21 18:12:07,448 INFO sqlalchemy.engine.base.Engine COMMIT

Then

    MariaDB [tester]> SELECT * FROM page;
    +----+--------------+---------------------+-----------+---------+
    | id | content      | posted              | title     | heading |
    +----+--------------+---------------------+-----------+---------+
    |  1 | Test Content | 2016-02-21 18:11:59 | Test Page | NULL    |
    +----+--------------+---------------------+-----------+---------+
    1 row in set (0.00 sec)

### Delete

And

    In [12]: session.delete(test_page)
    
    In [13]: session.flush()
    2016-02-21 18:13:23,996 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)
    2016-02-21 18:13:23,998 INFO sqlalchemy.engine.base.Engine SELECT page.id AS page_id, page.content AS page_content, page.posted AS page_posted, page.title AS page_title, page.heading AS page_heading
    FROM page
    WHERE page.id = %s
    2016-02-21 18:13:23,998 INFO sqlalchemy.engine.base.Engine (1,)
    2016-02-21 18:13:24,004 INFO sqlalchemy.engine.base.Engine SELECT comment.id AS comment_id, comment.pageid AS comment_pageid, comment.content AS comment_content, comment.name AS comment_name, comment.email AS comment_email, comment.created AS comment_created
    FROM comment
    WHERE %s = comment.pageid
    2016-02-21 18:13:24,005 INFO sqlalchemy.engine.base.Engine (1,)
    2016-02-21 18:13:24,011 INFO sqlalchemy.engine.base.Engine SELECT tag.id AS tag_id, tag.name AS tag_name
    FROM tag, pagetag
    WHERE %s = pagetag.pageid AND tag.id = pagetag.tagid
    2016-02-21 18:13:24,011 INFO sqlalchemy.engine.base.Engine (1,)
    2016-02-21 18:13:24,013 INFO sqlalchemy.engine.base.Engine DELETE FROM page WHERE page.id = %s
    2016-02-21 18:13:24,013 INFO sqlalchemy.engine.base.Engine (1,)

But, suppose we don't want to keep that change. Then, instead of `commit()`:

    In [15]: session.rollback()
    2016-02-21 18:13:38,282 INFO sqlalchemy.engine.base.Engine ROLLBACK

### Query

Queries are performed with query objects that created from the session.

    In [16]: page_q = session.query(model.Page)
    
    In [17]: for page in page_q:
       ....:     print page.title
       ....:
    2016-02-21 18:15:19,222 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)
    2016-02-21 18:15:19,223 INFO sqlalchemy.engine.base.Engine SELECT page.id AS page_id, page.content AS page_content, page.posted AS page_posted, page.title AS page_title, page.heading AS page_heading
    FROM page
    2016-02-21 18:15:19,223 INFO sqlalchemy.engine.base.Engine ()
    Test Page
    
    In [18]: page_q.all()
    2016-02-21 18:15:27,046 INFO sqlalchemy.engine.base.Engine SELECT page.id AS page_id, page.content AS page_content, page.posted AS page_posted, page.title AS page_title, page.heading AS page_heading
    FROM page
    2016-02-21 18:15:27,047 INFO sqlalchemy.engine.base.Engine ()
    Out[18]: [<model.Page at 0x1042d9cd0>]
    
    In [19]: page = page_q.first()
    2016-02-21 18:15:39,732 INFO sqlalchemy.engine.base.Engine SELECT page.id AS page_id, page.content AS page_content, page.posted AS page_posted, page.title AS page_title, page.heading AS page_heading
    FROM page
     LIMIT %s
     2016-02-21 18:15:39,733 INFO sqlalchemy.engine.base.Engine (1,)
    
    In [20]: page.title
    Out[20]: u'Test Page'
    
    In [21]: page_q[2:5]
    2016-02-21 18:15:51,135 INFO sqlalchemy.engine.base.Engine SELECT page.id AS page_id, page.content AS page_content, page.posted AS page_posted, page.title AS page_title, page.heading AS page_heading
    FROM page
    LIMIT %s, %s
    2016-02-21 18:15:51,135 INFO sqlalchemy.engine.base.Engine (2, 3)
    Out[21]: []
    
    In [22]: page_q.get(1)
    Out[22]: <model.Page at 0x1042d9cd0>

### Workign with Objects

How to add a comment to a page? The Object-Relational API provides a nice
approach:

    In [23]: comment1 = model.Comment()
    
    In [24]: comment1.name = u'James'
    
    In [25]: comment1.email = u'james@example.com'
    
    In [26]: comment1.content = u'This page needs detail.'
    
    In [27]: comment2 = model.Comment()
    
    In [28]: comment2.name = u'Mike'
    
    In [29]: comment2.email = u'mike@example.com'
    
    In [30]: page.comments.append(comment1)
    2016-02-21 18:19:08,780 INFO sqlalchemy.engine.base.Engine SELECT comment.id AS comment_id, comment.pageid AS comment_pageid, comment.content AS comment_content, comment.name AS comment_name, comment.email AS comment_email, comment.created AS comment_created
    FROM comment
    WHERE %s = comment.pageid
    2016-02-21 18:19:08,780 INFO sqlalchemy.engine.base.Engine (1,)
    
    In [31]: page.comments.append(comment2)
    
    In [32]: session.commit()
    2016-02-21 18:19:17,508 INFO sqlalchemy.engine.base.Engine INSERT INTO comment (pageid, content, name, email, created) VALUES (%s, %s, %s, %s, %s)
    2016-02-21 18:19:17,509 INFO sqlalchemy.engine.base.Engine (1, u'This page needs detail.', u'James', u'james@example.com', datetime.datetime(2016, 2, 21, 18, 19, 17, 508721))
    2016-02-21 18:19:17,511 INFO sqlalchemy.engine.base.Engine INSERT INTO comment (pageid, content, name, email, created) VALUES (%s, %s, %s, %s, %s)
    2016-02-21 18:19:17,511 INFO sqlalchemy.engine.base.Engine (1, u'', u'Mike', u'mike@example.com', datetime.datetime(2016, 2, 21, 18, 19, 17, 511023))
    2016-02-21 18:19:17,512 INFO sqlalchemy.engine.base.Engine COMMIT

Rather than having to manually set each comment's `.pageid` attribute, we append
the comments to the page's `.comments` attribute. We didn't need to explicitly
add the comments to the session - SQLAlchemy was smart enough to realize that
they have been appended to an object already in the session.

    MariaDB [tester]> SELECT * FROM comment\G
    *************************** 1. row ***************************
         id: 1
     pageid: 1
    content: This page needs detail.
       name: James
      email: james@example.com
    created: 2016-02-21 18:19:17
    *************************** 2. row ***************************
         id: 2
     pageid: 1
    content:
       name: Mike
      email: mike@example.com
    created: 2016-02-21 18:19:17
    2 rows in set (0.00 sec)

