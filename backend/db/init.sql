USE online_library;

CREATE TABLE IF NOT EXISTS Utilisateur (UID char(200), nom varchar(200), date_naissance DATE, telephone varchar(20), adresse varchar(255)
                                       , date_creation DATETIME DEFAULT CURRENT_TIMESTAMP, mot_de_passe varchar(255), email varchar(200),
                                        PRIMARY KEY (UID));

CREATE TABLE IF NOT EXISTS client (UID char(200), PRIMARY KEY (UID), FOREIGN KEY (UID) REFERENCES Utilisateur(UID)
                                  ON UPDATE CASCADE
                                  ON DELETE CASCADE );


CREATE TABLE IF NOT EXISTS Administrateur (UID char(200), PRIMARY KEY (UID), FOREIGN KEY (UID) REFERENCES Utilisateur(UID)
                                  ON UPDATE CASCADE
                                  ON DELETE CASCADE );

CREATE TABLE IF NOT EXISTS Livre (ISBN char(200),nom varchar(255), genre varchar(100), description TEXT,
                                    URL_couverture varchar(500), URL_du_contenu varchar(500), note integer,
                                    PRIMARY KEY (ISBN));

CREATE TABLE IF NOT EXISTS Commentaire (date_publication DATETIME, CID char(200), message TEXT,
                                    PRIMARY KEY (CID));

CREATE TABLE IF NOT EXISTS Publier (Uid char(200), CID char(200),
                                    PRIMARY KEY (Uid,CID),
                                    FOREIGN KEY (Uid) REFERENCES Utilisateur(UID)
                                   ON UPDATE CASCADE
                                   ON DELETE CASCADE ,
                                    FOREIGN KEY (CID) REFERENCES Commentaire(CID)
                                   ON UPDATE CASCADE
                                   ON DELETE CASCADE );

CREATE TABLE IF NOT EXISTS Recevoir (ISBN char(200), CID char(200),
                                    PRIMARY KEY (ISBN,CID),
                                    FOREIGN KEY (ISBN) REFERENCES Livre(ISBN)
                                   ON UPDATE CASCADE
                                   ON DELETE CASCADE ,
                                    FOREIGN KEY (CID) REFERENCES Commentaire(CID)
                                   ON UPDATE CASCADE
                                   ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS Noter (
    LID char(200),
    UID char(200),
    Note integer,
    PRIMARY KEY (LID, UID),
    FOREIGN KEY (LID) REFERENCES Livre(ISBN)
        ON UPDATE CASCADE
        ON DELETE CASCADE, -- Cette virgule est correcte car une autre contrainte suit
    FOREIGN KEY (UID) REFERENCES Utilisateur(UID)
        ON UPDATE CASCADE
        ON DELETE CASCADE  -- <--- PAS DE VIRGULE ICI
);

CREATE TABLE IF NOT EXISTS Consulter (LID char(200), UID char(200), Date_de_consultation DATETIME DEFAULT CURRENT_TIMESTAMP, Derniere_page_consultee integer,
                                PRIMARY KEY (LID, UID),
                                FOREIGN KEY (LID) REFERENCES Livre(ISBN)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE,
                                 FOREIGN KEY (UID) REFERENCES Utilisateur(UID)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS Suit (LID char(200), UID char(200), Favoris boolean,
                                PRIMARY KEY (LID, UID),
                                FOREIGN KEY (LID) REFERENCES Livre(ISBN)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE,
                                 FOREIGN KEY (UID) REFERENCES Utilisateur(UID)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE);


CREATE TABLE IF NOT EXISTS Auteur (AID char(200), Description char(200),
                                PRIMARY KEY (AID));

CREATE TABLE IF NOT EXISTS Ecrit (AID char(200), ISBN char(200),
                                 PRIMARY KEY (AID,ISBN),
                                 FOREIGN KEY (AID) REFERENCES Auteur(AID)
                                 ON UPDATE CASCADE
                                 ON DELETE CASCADE,
                                 FOREIGN KEY (ISBN) REFERENCES Livre(ISBN)
                                 ON UPDATE CASCADE
                                 ON DELETE CASCADE
                                 );

CREATE TABLE IF NOT EXISTS Editeur (PID char(200), Description char(200)
                                   ,PRIMARY KEY (PID));

CREATE TABLE IF NOT EXISTS Publie (PID char(200), ISBN char(200), Date_de_Publication DATE,
                                 PRIMARY KEY (PID,ISBN),
                                 FOREIGN KEY (PID) REFERENCES Editeur(PID)
                                 ON UPDATE CASCADE
                                 ON DELETE CASCADE,
                                 FOREIGN KEY (ISBN) REFERENCES Livre(ISBN)
                                 ON UPDATE CASCADE
                                 ON DELETE CASCADE);

