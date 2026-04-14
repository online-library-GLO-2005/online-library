from dataclasses import dataclass

from dataclasses import dataclass

@dataclass
class Publisher:
    TABLE = "Editeur"

    class Columns:
        ID = "EID"
        NAME = "nom"
        DESCRIPTION = "description"

    id: int
    name: str
    description: str = None

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        return cls(
            id=data.get(cls.Columns.ID),
            name=data.get(cls.Columns.NAME),
            description=data.get(cls.Columns.DESCRIPTION)
        )