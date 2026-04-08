from abc import ABC, abstractmethod
from app.errors import AppError


class OwnableService(ABC):
    """
    Only classes that have User as owners inherit this one
    """

    @abstractmethod
    def get_owner_id(self, resource_id: str) -> str:
        """Return the user_id of the resource owner"""
        pass
