USE online_library;

/* Seed data for admin table */
-- hashed password (with bcrypt): adminpassword
CALL sp_creer_admin('admin', 'admin@gmail.com', '$2b$12$A.3Ar7iZjhXSXpBj9pA02.g.0vlKuW0pM0ymmpwHkdWF38VjuBl2m');

/* Seed data for Client table */
-- hashed password (with bcrypt): example
CALL sp_inscrire_client('Example', 'example@gmail.com', '$2b$12$de8uKV2IBjsjx6XbyJXj9.uvuWBWh4tTsj.2/BCba.Wz121q48zdO');


/* Seed data for Genre table */
INSERT IGNORE INTO Genre (nom) VALUES ('Science-Fiction');
INSERT IGNORE INTO Genre (nom) VALUES ('Roman');
INSERT IGNORE INTO Genre (nom) VALUES ('Thriller');
INSERT IGNORE INTO Genre (nom) VALUES ('Fantasy');
INSERT IGNORE INTO Genre (nom) VALUES ('Horreur');
INSERT IGNORE INTO Genre (nom) VALUES ('Mystère');
INSERT IGNORE INTO Genre (nom) VALUES ('Aventure');
INSERT IGNORE INTO Genre (nom) VALUES ('Historique');
INSERT IGNORE INTO Genre (nom) VALUES ('Biographie');
INSERT IGNORE INTO Genre (nom) VALUES ('Autobiographie');
INSERT IGNORE INTO Genre (nom) VALUES ('Philosophie');
INSERT IGNORE INTO Genre (nom) VALUES ('Poésie');
INSERT IGNORE INTO Genre (nom) VALUES ('Conte');
INSERT IGNORE INTO Genre (nom) VALUES ('Nouvelle');
INSERT IGNORE INTO Genre (nom) VALUES ('Policier');
INSERT IGNORE INTO Genre (nom) VALUES ('Romance');
INSERT IGNORE INTO Genre (nom) VALUES ('Science');
INSERT IGNORE INTO Genre (nom) VALUES ('Psychologie');
INSERT IGNORE INTO Genre (nom) VALUES ('Développement personnel');
INSERT IGNORE INTO Genre (nom) VALUES ('Jeunesse');
INSERT IGNORE INTO Genre (nom) VALUES ('Bande dessinée');
INSERT IGNORE INTO Genre (nom) VALUES ('Manga');
INSERT IGNORE INTO Genre (nom) VALUES ('Classique');
INSERT IGNORE INTO Genre (nom) VALUES ('Dystopie');
INSERT IGNORE INTO Genre (nom) VALUES ('Utopie');


/* Seed data for Editeur table */
INSERT IGNORE INTO Editeur (nom, description) VALUES ('Example', 'This is an example of a description for the publisher Example');
INSERT IGNORE INTO Editeur (nom, description) VALUES ('Gallimard', 'Maison d\'édition française fondée en 1911');
INSERT IGNORE INTO Editeur (nom, description) VALUES ('Hachette', 'Groupe d\'édition français');


/* Seed data for Auteur table */
INSERT IGNORE INTO Auteur (nom, description) VALUES ('Example', 'This is an example of a description of the author Example');
INSERT IGNORE INTO Auteur (nom, description) VALUES ('Me Myself and I', 'This is a description of the author Me Myself and I');
INSERT IGNORE INTO Auteur (nom, description) VALUES ('Victor Hugo', 'Auteur français du 19e siècle');
INSERT IGNORE INTO Auteur (nom, description) VALUES ('J.K. Rowling', 'Auteure de Harry Potter');


/* Seed data for Livre table */
INSERT IGNORE INTO Livre (EID, ISBN, nom, description, url_couverture, url_contenu, date_publication)
VALUES (
    (SELECT EID FROM Editeur WHERE nom = 'Example'),
    '000-0-00-000000-0',                      -- ISBN example
    'Nicolas\' rant',                         -- nom
    'Un chef-d\'oeuvre de Me Myself and I',       -- description
    'http://localhost:5000/media/covers/exampleCover.jpg',  -- url_couverture
    'http://localhost:5000/media/books/exampleBook.pdf',      -- url_contenu
    '2026-04-13'                              -- date_publication -- actual date of the edit
);

INSERT IGNORE INTO Ecrit (AID, LID)
VALUES (
    (SELECT AID FROM Auteur WHERE nom = 'Me Myself and I'),
    (SELECT LID FROM Livre WHERE nom = 'Nicolas\' rant')
);

INSERT IGNORE INTO Classer (GID, LID)
VALUES (
    (SELECT GID FROM Genre WHERE nom = 'Philosophie'),
    (SELECT LID FROM Livre WHERE nom = 'Nicolas\' rant')
);

INSERT IGNORE INTO Noter (UID, LID, note)
VALUES (
    (SELECT UID FROM Utilisateur WHERE email = 'example@gmail.com'),
    (SELECT LID FROM Livre WHERE nom = 'Nicolas\' rant'),
    4.5
);

INSERT IGNORE INTO Commentaire (UID, LID, message)
VALUES (
    (SELECT UID FROM Utilisateur WHERE email = 'example@gmail.com'),
    (SELECT LID FROM Livre WHERE nom = 'Nicolas\' rant'),
    'Ah, mais quelle bonne critique et rant de projet. Quelle originalité ! J\'ai adoré la plume de Me Myself and I, c\'est un vrai plaisir à lire. J\'ai ri, j\'ai pleuré, j\'ai même eu des moments de réflexion profonde sur la vie grâce à ce livre. Un chef-d\'oeuvre qui mérite d\'être lu par tous les amateurs de philosophie et de littérature en général.'
);

INSERT IGNORE INTO Commentaire (UID, LID, message)
VALUES (
    (SELECT UID FROM Utilisateur WHERE email = 'admin@gmail.com'),
    (SELECT LID FROM Livre WHERE nom = 'Nicolas\' rant'),
    'Send help please. What a project to have taken on for a database course. I\'m drowning in SQL, in python, and in React and I can\'t find my way out. The only thing that keeps me going is the hope that one day, when this is all over, I\'ll be able to look back at this and laugh. But right now, it just feels like I\'m stuck in an endless loop of CREATE TABLE, INSERT INTO, and SELECT * FROM. Send help.'
);

INSERT IGNORE INTO Suit (UID, LID, favoris)
VALUES (
    (SELECT UID FROM Utilisateur WHERE email = 'example@gmail.com'),
    (SELECT LID FROM Livre WHERE nom = 'Nicolas\' rant'),
    TRUE
);

INSERT IGNORE INTO Consulter (UID, LID)
VALUES (
    (SELECT UID FROM Utilisateur WHERE email = 'example@gmail.com'),
    (SELECT LID FROM Livre WHERE nom = 'Nicolas\' rant')
);
