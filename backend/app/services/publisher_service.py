from app.repositories.publisher_repo import publisher_repo
from app.repositories.book_repo import book_repo
from app.errors import AppError


class PublisherService:
    def __init__(self):
        self._repo = publisher_repo

    def get_all_publishers(self):
        return self._repo.get_all()

    def get_publisher_by_id(self, eid: int):
        publisher = self._repo.get_by_id(eid)
        if not publisher:
            raise AppError(404, "Éditeur introuvable")
        return publisher

    def create_publisher(self, data: dict):
        return self._repo.create(data["name"], data.get("description"))

    def update_publisher(self, eid: int, data: dict):
        self.get_publisher_by_id(eid)
        self._repo.update(eid, data["name"], data.get("description"))
        return self._repo.get_by_id(eid)

    def delete_publisher(self, eid: int):
        self.get_publisher_by_id(eid)
        books = book_repo.find_by_publisher(publisher_id)
        if books:
            raise AppError(409, "Cannot delete publisher: books are still linked to it")
        self._repo.delete(eid)


publisher_service = PublisherService()
