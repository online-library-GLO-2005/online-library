from dataclasses import dataclass
from datetime import datetime

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Comment:
    TABLE = "Commentaire"  # Correspond au nom dans ton CREATE TABLE

    class Columns:
        ID = "CID"                   # Clé primaire
        UID = "UID"                  # Clé étrangère Utilisateur
        LID = "LID"                  # Clé étrangère Livre
        MESSAGE = "message"           # TEXT NOT NULL
        DATE = "date_publication"     # DATETIME

    id: int
    uid: int
    lid: int
    message: str
    date_publication: datetime

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        return cls(
            id=data.get(cls.Columns.ID),
            uid=data.get(cls.Columns.UID),
            lid=data.get(cls.Columns.LID),
            message=data.get(cls.Columns.MESSAGE),
            date_publication=data.get(cls.Columns.DATE)
        )