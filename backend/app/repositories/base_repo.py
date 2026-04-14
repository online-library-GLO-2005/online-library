from app.infrastructure.db import database
from app.models.user import User


class BaseRepo:
    def __init__(self):
        self._db = database
