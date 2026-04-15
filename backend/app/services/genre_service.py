from app.repositories.genre_repo import genre_repo
from app.errors import AppError


class GenreService:
    def __init__(self):
        self._repo = genre_repo

    def get_all_genres(self):
        return self._repo.get_all()

    def get_genre_by_id(self, gid: int):
        genre = self._repo.get_by_id(gid)
        if not genre:
            raise AppError(404, "Genre introuvable")
        return genre

    def create_genre(self, name: str):
        return self._repo.create(name)

    def update_genre(self, gid: int, name: str):
        self.get_genre_by_id(gid)
        self._repo.update(gid, name)
        return self._repo.get_by_id(gid)

    def delete_genre(self, gid: int):
        self.get_genre_by_id(gid)
        self._repo.delete(gid)

    def get_books_by_genre(self, gid: int):
        return self._repo.get_books_by_genre(gid)



genre_service = GenreService()
