"""Implements MySQL database connectivity for the LCC Issue Tracker.

This approach is based on the Flask tutorial "Define and Access the Database",
adapted to use MySQL with connection pooling.
"""
from flask import Flask, g
from mysql.connector.pooling import MySQLConnectionPool

# Pool of reusable database connections
connection_pool = None

def init_db(app: Flask, user: str, password: str, host: str, database: str,
            pool_name: str = "flask_db_pool", autocommit: bool = True):
    """Sets up a MySQL connection pool for the specified Flask app.

    Args:
        app: The Flask application to set up database connectivity for.
        user: Username used to connect to the MySQL server.
        password: Password used to connect to the MySQL server.
        host: Host name or IP address of the MySQL server.
        database: Name of the database to connect to on the MySQL server.
        pool_name: Name of the pool to create (default `flask_db_pool`).
        autocommit: Whether or not to enable auto-commit (default `True`).
    """
    # Create a pool of reusable database connections.
    global connection_pool
    connection_pool = MySQLConnectionPool(
        user=user,
        password=password,
        host=host,
        database=database,
        pool_name=pool_name,
        autocommit=autocommit)

    # Register `close_db()` to run every time the application context is torn
    # down at the end of a Flask request, ensuring that any database connection
    # using during that request gets released back into the pool.
    app.teardown_appcontext(close_db)

def get_db():
    """Gets a MySQL database connection to use while serving the current Flask
    request.

    The first time you call this during a request, a new connection will be
    allocated from the pool. After that, any additional calls to `get_db()`
    during the same request are guaranteed to return the same connection.
    
    You don't need to manually close the connection returned by `get_db()` - it
    will be returned to the pool automatically at the end of the Flask request.
    However, you should be sure to close any cursors that you create.

    Returns:
        A `PooledMySQLConnection` instance.
    """
    if 'db' not in g:
        g.db = connection_pool.get_connection()
    
    return g.db

def get_cursor():
    """Gets a new MySQL dictionary cursor to use while serving the current
    Flask request.
    
    All cursors created by this function during a single Flask request will
    belong to the same connection. You can get a reference to that connection
    at any time during the request by calling `get_db()`.
    
    Ensure that you close all cursors before the end of the Flask request.
    
    Returns:
        A new `MySQLCursor` instance.
    """
    return get_db().cursor(dictionary=True)

def close_db(exception = None):
    """Closes the MySQL database connection associated with the current Flask
    request (if any).
    
    There should be no need to call this manually: this function is called
    automatically when the application context is torn down at the end of each
    Flask request.

    Args:
        exception: The exception that terminated the Flask request, or `None`
            if the request terminated successfully.
    """
    # Get the database connection from the current application context (the one
    # that's being torn down), or `None` if there is no connection.
    db = g.pop('db', None)
    
    if db is not None:
        db.close()