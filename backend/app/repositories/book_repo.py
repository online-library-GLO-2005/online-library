from app.extensions import get_connection
from app.utils.errors import AppError

def get_all_books():
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, author_id FROM books")
            return cursor.fetchall()
    except Exception:
        raise AppError("Database error")

def create_book(title, author_id):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO books (title, author_id) VALUES (%s, %s)"
            cursor.execute(sql, (title, author_id))
    except Exception:
        raise AppError("Database error")