from faker import Faker
import random
import os
from reportlab.pdfgen import canvas

# Tes imports de repos
from app.repositories.book_repo import book_repo
from app.repositories.author_repo import author_repo
from app.repositories.genre_repo import genre_repo
from app.repositories.publisher_repo import publisher_repo
from app.repositories.comment_repo import comment_repo
from app.repositories.user_repo import user_repo
from app.repositories.auth_repo import auth_repo

from app.utils.security import hashPassword


class DatabaseSeeder:
    def __init__(self):
        self.faker = Faker(['fr_FR'])

    def generate_dummy_pdf(self, file_path, title):
        """Génère physiquement un PDF dans le volume Docker"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        c = canvas.Canvas(file_path)
        c.drawString(100, 750, f"Contenu de démonstration pour : {title}")
        c.drawString(100, 730, f"Titre : {title}")
        c.drawString(100, 710, "Projet : Bibliothèque en ligne - GLO-2005 (ULaval)")
        c.save()

    def seed(self):
        print("Début du peuplement de la base de données...")

        # 1. Genres
        genres = ["Science-Fiction", "Roman", "Policier", "Historique", "Biographie", "Fantastique"]
        genre_ids = [genre_repo.create(g).id for g in genres]

        # 2. Éditeurs
        editeur_ids = [publisher_repo.create(self.faker.company(), self.faker.catch_phrase()).id for _ in range(10)]

        # 3. Auteurs
        author_ids = []
        for _ in range(30):
            author = author_repo.create({
                'name': self.faker.name(),
                'description': self.faker.text(max_nb_chars=200),
                'photo_url': self.faker.image_url()
            })
            author_ids.append(author.id)

        # 4. Livres et fichiers PDF
        book_ids = []
        print("Génération des livres et des fichiers PDF...")
        for i in range(120):
            title = self.faker.sentence(nb_words=4)
            file_name = f"livre_{i}.pdf"

            # 1. Chemin physique (pour l'écriture sur le disque/volume)
            file_path = os.path.join(os.getcwd(), 'media', 'books', file_name)
            self.generate_dummy_pdf(file_path, title)

            # 2. URL relative (pour le stockage en base de données)
            # On suit le format de la route media : /media/books/nom_du_fichier
            relative_url = f"/media/books/{file_name}"

            book = book_repo.create_book({
                'eid': random.choice(editeur_ids),
                'isbn': self.faker.isbn13(),
                'title': title,
                'description': self.faker.paragraph(nb_sentences=3),
                'cover_url': self.faker.image_url(),  # On pourrait faire pareil pour les covers si nécessaire
                'content_url': relative_url,  # Ici on met l'URL complète
                'pub_date': self.faker.date_between(start_date='-10y', end_date='today')
            })
            book_ids.append(book.id)
            # Liaisons
            for aid in random.sample(author_ids, k=random.randint(1, 2)):
                book_repo.link_author(book.id, aid)
            for gid in random.sample(genre_ids, k=random.randint(1, 3)):
                book_repo.link_genre(book.id, gid)

        # 5. Utilisateurs
        print("Création des utilisateurs...")
        user_ids = []
        hashed_password = hashPassword('password123')
        for _ in range(50):
            user = auth_repo.register(
                self.faker.name(),
                self.faker.unique.email(),
                hashed_password
            )
            if user:
                user_ids.append(user.id)

        # Admin
        if user_ids:
            auth_repo.promote_to_admin(user_ids[0])

        # 6. Interactions (Commentaires et Favoris)
        print("Ajout des commentaires et favoris...")
        for bid in book_ids:
            # Commentaires
            num_comments = random.randint(1, 3)
            selected_uids = random.sample(user_ids, k=min(num_comments, len(user_ids)))
            for uid in selected_uids:
                comment_repo.create(
                    user_id=uid,
                    book_id=bid,
                    message=self.faker.sentence(nb_words=12)
                )

            # Favoris
            lucky_users = random.sample(user_ids, k=random.randint(0, min(3, len(user_ids))))
            for uid in lucky_users:
                user_repo.add_to_favorites(uid, bid)

        print(" Peuplement terminé avec succès !")


if __name__ == "__main__":
    seeder = DatabaseSeeder()
    seeder.seed()