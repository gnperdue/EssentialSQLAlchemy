# Testing

How do we perform functional tests against a database? How do we mock out
SQLAlchemy queries and connections?

## Testing with a Test Database

For our example application, we will have an `app.py` that contains the
application logic and a `db.py` that contains the database tables and
connections.
