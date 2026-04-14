from dataclasses import dataclass

@dataclass
class Author:
    TABLE = "Auteur"

    class Columns:
        ID = "AID"
        NAME = "nom"
        DESCRIPTION = "description"
        PHOTO_URL = "url_photo"

    id: int
    name: str
    description: str = None
    photo_url: str = None

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        return cls(
            id=data.get(cls.Columns.ID),
            name=data.get(cls.Columns.NAME),
            description=data.get(cls.Columns.DESCRIPTION),
            photo_url=data.get(cls.Columns.PHOTO_URL)
        )