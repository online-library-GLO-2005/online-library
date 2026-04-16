from faker import Faker
import random
from app.repositories.book_repo import book_repo
from app.repositories.author_repo import author_repo
from app.repositories.genre_repo import genre_repo
from app.repositories.publisher_repo import publisher_repo  # Si tu l'as créé

from app.repositories.comment_repo import comment_repo
from app.repositories.user_repo import user_repo

from app.repositories.auth_repo import auth_repo

from app.utils.security import hashPassword


class DatabaseSeeder:
    def __init__(self):
        self.faker = Faker(['fr_FR'])  # Pour avoir des noms et textes en français

    def seed(self):
        print("Début du peuplement de la base de données...")

        # 1. Créer des Genres
        genres = ["Science-Fiction", "Roman", "Policier", "Historique", "Biographie", "Fantastique"]
        genre_ids = []
        for g_name in genres:
            genre = genre_repo.create(g_name)
            genre_ids.append(genre.id)

        # 2. Créer des Éditeurs
        editeur_ids = []
        for _ in range(20):
            editeur = publisher_repo.create(
                name=self.faker.company(),
                description=self.faker.catch_phrase()
            )
            editeur_ids.append(editeur.id)

        # 3. Créer des Auteurs
        author_ids = []
        for _ in range(50):
            author = author_repo.create({
                'name': self.faker.name(),
                'description': self.faker.text(max_nb_chars=200),
                'photo_url': self.faker.image_url()
            })
            author_ids.append(author.id)

        # 4. Créer des Livres et faire les liaisons
        # Dans ton fichier auto_populate.py
        book_ids = []
        for _ in range(60):
            # Appel de la méthode avec le bon nom : create_book
            book = book_repo.create_book({
                'eid': random.choice(editeur_ids),
                'isbn': self.faker.isbn13(),
                'title': self.faker.sentence(nb_words=4),
                'description': self.faker.paragraph(nb_sentences=3),
                'cover_url': self.faker.image_url(),
                'content_url': self.faker.url(),
                'pub_date': self.faker.date_between(start_date='-10y', end_date='today')
            })
            book_ids.append(book.id)
            # Liaison aléatoire : 1 à 2 auteurs par livre
            selected_authors = random.sample(author_ids, k=random.randint(1, 2))
            for aid in selected_authors:
                book_repo.link_author(book.id, aid)  # Utilise la table 'Ecrit'

            # Liaison aléatoire : 1 à 3 genres par livre
            selected_genres = random.sample(genre_ids, k=random.randint(1, 3))
            for gid in selected_genres:
                book_repo.link_genre(book.id, gid)  # Utilise la table 'Classer'

        print("Création des utilisateurs via la procédure stockée...")
        user_ids = []
        password_clair = 'password123'
        hashed_password = hashPassword(password_clair)
        for _ in range(20):
            # Attention : AuthRepo.register(name, email, hashed_password)
            # Pour le seeder, on peut mettre un mot de passe en clair ou simulé
            user = auth_repo.register(
                self.faker.name(),
                self.faker.unique.email(),
                hashed_password
            )

            if user:
                user_ids.append(user.id)

        # Promouvoir le premier utilisateur en admin pour tes tests
        if user_ids:
            auth_repo.promote_to_admin(user_ids[0])
            print(f"Utilisateur {user_ids[0]} promu administrateur !")

        # 6. Créer des Commentaires et des Favoris
        print("Ajout des interactions...")
        for bid in book_ids:
            # On détermine combien de commentaires on veut
            num_comments = random.randint(1, 3)

            # On choisit 'num_comments' utilisateurs UNIQUES parmi notre liste
            if len(user_ids) >= num_comments:
                selected_uids = random.sample(user_ids, k=num_comments)
            else:
                selected_uids = user_ids

            for uid in selected_uids:
                comment_repo.create(
                    user_id=uid,
                    book_id=bid,
                    message=self.faker.sentence(nb_words=12)
                )

            # Ajouter en favoris (déjà correct car random.sample garantit l'unicité)
            num_favs = random.randint(0, min(4, len(user_ids)))
            lucky_users = random.sample(user_ids, k=num_favs)
            for uid in lucky_users:
                user_repo.add_to_favorites(uid, bid)
        print("Peuplement terminé avec succès !")


# Pour l'exécuter
if __name__ == "__main__":
    seeder = DatabaseSeeder()
    seeder.seed()