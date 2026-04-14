from dataclasses import dataclass
from datetime import date

@dataclass
class Book:
    TABLE = "Livre"

    class Columns:
        ID = "LID"
        EID = "EID"
        ISBN = "ISBN"
        TITLE = "nom"
        DESCRIPTION = "description"
        COVER_URL = "url_couverture"
        CONTENT_URL = "url_contenu"
        RATING = "note"
        PUB_DATE = "date_publication"

    id: int
    eid: int
    isbn: str
    title: str
    pub_date: date
    description: str = None
    cover_url: str = None
    content_url: str = None
    rating: float = None

    @classmethod
    def from_dict(cls, data: dict):
        """Crée une instance de Book à partir d'un dictionnaire de la DB."""
        return cls(
            id=data.get(cls.Columns.ID),
            eid=data.get(cls.Columns.EID),
            isbn=data.get(cls.Columns.ISBN),
            title=data.get(cls.Columns.TITLE),
            pub_date=data.get(cls.Columns.PUB_DATE),
            description=data.get(cls.Columns.DESCRIPTION),
            cover_url=data.get(cls.Columns.COVER_URL),
            content_url=data.get(cls.Columns.CONTENT_URL),
            rating=data.get(cls.Columns.RATING)
        )