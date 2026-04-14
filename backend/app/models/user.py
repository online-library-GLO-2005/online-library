from dataclasses import dataclass
from datetime import date, datetime

@dataclass
class User:
    TABLE = "Utilisateur"

    class Columns:
        ID = "UID"
        NAME = "nom"
        EMAIL = "email"
        PASSWORD = "mot_de_passe_hash"
        BIRTH_DATE = "date_naissance"
        PHONE = "telephone"
        ADDRESS = "adresse"
        CREATED_AT = "date_creation_compte"

    id: int
    name: str
    email: str
    password_hash: str
    birth_date: date = None
    phone: str = None
    address: str = None
    created_at: datetime = None

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        return cls(
            id=data.get(cls.Columns.ID),
            name=data.get(cls.Columns.NAME),
            email=data.get(cls.Columns.EMAIL),
            password_hash=data.get(cls.Columns.PASSWORD),
            birth_date=data.get(cls.Columns.BIRTH_DATE),
            phone=data.get(cls.Columns.PHONE),
            address=data.get(cls.Columns.ADDRESS),
            created_at=data.get(cls.Columns.CREATED_AT)
        )