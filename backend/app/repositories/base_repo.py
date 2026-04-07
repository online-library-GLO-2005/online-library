from app.infrastructure.db import Database


class BaseRepo:
    def __init__(self):
        self._db = Database()
