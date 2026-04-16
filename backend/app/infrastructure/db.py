from contextlib import contextmanager
from typing import Generator, Any, cast
from pymysql.connections import Connection
from pymysqlpool import ConnectionPool
from pymysql.cursors import DictCursor
from app.errors import AppError
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

        host = os.getenv("MYSQL_HOST", "localhost")
        port = int(os.getenv("MYSQL_PORT", "3306"))
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        database = os.getenv("MYSQL_DATABASE", "mydb")

        if not user or not password:
            raise RuntimeError("Missing .env: MYSQL_USER or MYSQL_PASSWORD")

        self._pool = ConnectionPool(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            size=5,
            maxsize=10,
            autocommit=True,
            cursorclass=DictCursor,
        )

        self._initialized = True

    @contextmanager
    def _get_conn(self) -> Generator[Connection, None, None]:
        conn = self._pool.get_connection()
        try:
            yield conn
        finally:
            conn.close()

    @contextmanager
    # Provides a transaction context for multi-step writes
    def transaction(self) -> Generator[Connection, None, None]:
        with self._get_conn() as conn:
            conn.autocommit(False)  # Critical — pool default is True
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.autocommit(True)  # Restore for pool reuse

    # params replaces %s placeholders in queries: "SELECT * FROM books WHERE id = %s", (1,)
    # returns first result as dict or None if not found: {"id": 1, "title": "Dune"}
    def execute(
            self,
            query: str,
            params: tuple[Any, ...] = (),
            conn: Connection | None = None,
            return_id: bool = False
    ) -> Any:
        if conn is None:
            with self._get_conn() as new_conn:
                return self._execute_internal(query, params, new_conn, return_id)
        return self._execute_internal(query, params, conn, return_id)

    def _execute_internal(
            self, query: str, params: tuple[Any, ...], conn: Connection, return_id: bool
    ) -> Any:
        with conn.cursor() as cursor:
            cursor.execute(query, params)

            if return_id:
                return cursor.lastrowid

            return cast(list[dict[str, Any]], cursor.fetchall())
    # params replaces %s placeholders in queries: "SELECT * FROM books WHERE id = %s", (1,)
    # returns first result as dict or None if not found: {"id": 1, "title": "Dune"}
    def execute_one(
        self, query: str, params: tuple[str, ...] = (), conn: Connection | None = None
    ) -> dict[str, Any] | None:
        if conn is not None:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cast(dict[str, Any] | None, cursor.fetchone())
        with self._get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cast(dict[str, Any] | None, cursor.fetchone())


# This is what we import
database = Database()
