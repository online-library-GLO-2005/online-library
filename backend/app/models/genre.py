from dataclasses import dataclass
@dataclass
class Genre:
    TABLE = "Genre"
    class Columns:
        ID = "GID"
        NAME = "nom"

    id: int
    name: str

    @classmethod
    def from_dict(cls, data: dict):
        if not data: return None
        return cls(
            id=data.get(cls.Columns.ID),
            name=data.get(cls.Columns.NAME)
        )