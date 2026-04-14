from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class User:
    TABLE = "Utilisateur"
    Admin_TABLE = "Administrateur"
    Client_TABLE = "Client"

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

        created_at = data.get(cls.Columns.CREATED_AT)

        if isinstance(created_at, str):
            try:
                created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                created_at = datetime.fromisoformat(created_at)

        birth_date = data.get(cls.Columns.BIRTH_DATE)
        if isinstance(birth_date, str):
            try:
                from datetime import date

                birth_date = date.fromisoformat(birth_date)
            except ValueError:
                birth_date = None

        return cls(
            id=data.get(cls.Columns.ID),
            name=data.get(cls.Columns.NAME),
            email=data.get(cls.Columns.EMAIL),
            password_hash=data.get(cls.Columns.PASSWORD),
            birth_date=birth_date,
            phone=data.get(cls.Columns.PHONE),
            address=data.get(cls.Columns.ADDRESS),
            created_at=created_at,
        )
