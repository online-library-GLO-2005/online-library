from app.repositories.genre_repo import genre_repo


class GenreService:
    def __init__(self):
        self._repo = genre_repo


genre_service = GenreService()
