from app.repositories.publisher_repo import publisher_repo


class PublisherService:
    def __init__(self):
        self._repo = publisher_repo


publisher_service = PublisherService()
