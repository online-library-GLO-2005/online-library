from contextlib import contextmanager
import pymysql.cursors
from pymysql.connections import Connection
import os

# Don't import this, use get_db() so that we don't have try catch everytime
def _get_connection() -> Connection:
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'), # MYSQL_HOST for docker and localhost for local
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )

@contextmanager
def get_db():
    connection = _get_connection()
    try:
        # yields when used with "with"
        yield connection
    finally:
        connection.close()