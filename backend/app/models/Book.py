from dataclasses import dataclass


# !!! THIS CLASS IS NOT COMPLETE, MERELY AN EXAMPLE TO BE FOLLOWED
# Represents the 'books' table structure.
# - Class-level constants (TABLE, Columns) are used in queries to avoid typos in column names.
# - Instance fields (id, title, isbn) represent a single row returned from the DB.
@dataclass
class Book:
    TABLE = "books"

    class Columns:
        ID = "id"
        TITLE = "title"
        ISBN = "isbn"

    id: int
    title: str
    isbn: str
