from dataclasses import dataclass
from datetime import datetime

@dataclass
class Comment:
    TABLE = "Commentaire"

    class Columns:
        ID = "CID"
        UID = "UID"
        LID = "LID"
        MESSAGE = "message"
        DATE = "date_publication"

    id: int
    uid: int
    lid: int
    message: str
    date_publication: datetime
    user_name: str = None

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        return cls(
            id=data.get(cls.Columns.ID),
            uid=data.get(cls.Columns.UID),
            lid=data.get(cls.Columns.LID),
            message=data.get(cls.Columns.MESSAGE),
            date_publication=data.get(cls.Columns.DATE),
            user_name=data.get('user_name')
        )