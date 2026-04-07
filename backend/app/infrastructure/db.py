from contextlib import contextmanager
from typing import Generator
from pymysql.connections import Connection
from pymysql.cursors import DictCursor
import pymysql
import os


# Singleton class that holds structure of conenction and execute method for mysql commands with pymysql
class Database:
    # Singleton
    _instance: "Database | None" = None

    # Start singleton with this method
    def __new__(cls) -> "Database":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized"):
            return

        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        database = os.getenv("MYSQL_DATABASE")

        if not user or not password or not database:
            raise RuntimeError("Missing required database environment variables")

        # After the check above, these are guaranteed to be str
        self.user: str = user
        self.password: str = password
        self.database: str = database
        # Use MYSQL_HOST env var = localhost if running mysql server locally and not through docker
        self.host: str = os.getenv("MYSQL_HOST", "localhost")
        self.port: int = int(os.getenv("MYSQL_PORT", "3306"))

        self._initialized = True

    # Connects to db wit user
    def _get_connection(self) -> Connection[DictCursor]:
        return pymysql.connect(  # type: ignore[call-overload]
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
            autocommit=True,
            cursorclass=DictCursor,
        )

    # returns Generator[YieldType, SendType, ReturnType]
    @contextmanager
    def _get_db(self) -> Generator[Connection[DictCursor], None, None]:
        connection = self._get_connection()
        try:
            # yields when used with "with"
            yield connection
        finally:
            connection.close()

    # params replaces %s placeholders in queries: "SELECT * FROM books WHERE id = %s", (1,)
    # returns first result as dict or None if not found: {"id": 1, "title": "Dune"}
    def execute(self, query: str, params: tuple = ()) -> list[dict]:
        with self._get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return list(cursor.fetchall())

    # params replaces %s placeholders in queries: "SELECT * FROM books WHERE id = %s", (1,)
    # returns first result as dict or None if not found: {"id": 1, "title": "Dune"}
    def execute_one(self, query: str, params: tuple = ()) -> dict | None:
        with self._get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
