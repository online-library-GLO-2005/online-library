-- This is done by Docker-compose. 
-- CREATE DATABASE IF NOT EXISTS online_library;
-- USE online_library;

-- TODO: Add indexes on foreign keys for better performance (e.g., EID in Livre, AID in Ecrit, GID in Classer, etc.)

-- ============================================================
-- 1. GENRE
-- ============================================================
CREATE TABLE IF NOT EXISTS Genre (
    GID  INT          NOT NULL AUTO_INCREMENT,
    nom  VARCHAR(100) NOT NULL,

    PRIMARY KEY (GID)
);

-- ============================================================
-- 2. AUTEUR
-- ============================================================
CREATE TABLE IF NOT EXISTS Auteur (
    AID          INT          NOT NULL AUTO_INCREMENT,
    nom          VARCHAR(100) NOT NULL,
    description  TEXT,
    url_photo    VARCHAR(255),

    PRIMARY KEY (AID)
);

-- ============================================================
-- 3. EDITEUR
-- ============================================================
CREATE TABLE IF NOT EXISTS Editeur (
    EID         INT          NOT NULL AUTO_INCREMENT,
    nom         VARCHAR(100) NOT NULL,
    description TEXT,

    PRIMARY KEY (EID)
);

-- ============================================================
-- 4. UTILISATEUR  (parent of Client, Administrateur, Refresh_tokens)
-- ============================================================

CREATE TABLE IF NOT EXISTS Utilisateur (
    UID                  INT          NOT NULL AUTO_INCREMENT,
    nom                  VARCHAR(100) NOT NULL,
    email                VARCHAR(255) NOT NULL UNIQUE,
    mot_de_passe_hash    VARCHAR(255) NOT NULL,
    date_naissance       DATE,
    telephone            VARCHAR(20),
    adresse              VARCHAR(255),
    date_creation_compte DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (UID)
);

-- ============================================================
-- 5. CLIENT  (ISA Utilisateur)
-- ============================================================
CREATE TABLE IF NOT EXISTS Client (
    UID INT NOT NULL,

    PRIMARY KEY (UID),
    CONSTRAINT fk_client_utilisateur
        FOREIGN KEY (UID) REFERENCES Utilisateur(UID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================
-- 6. ADMINISTRATEUR  (ISA Utilisateur)
-- ============================================================
CREATE TABLE IF NOT EXISTS Administrateur (
    UID INT NOT NULL,

    PRIMARY KEY (UID),
    CONSTRAINT fk_admin_utilisateur
        FOREIGN KEY (UID) REFERENCES Utilisateur(UID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================
-- 7. REFRESH_TOKENS
-- ============================================================
-- TODO: Implement delete token trigger to remove expired tokens
CREATE TABLE IF NOT EXISTS Refresh_tokens (
    TID         INT          NOT NULL AUTO_INCREMENT,
    UID         INT          NOT NULL,
    token_hash  VARCHAR(255) NOT NULL,
    expires_at  DATETIME     NOT NULL,
    revoked     BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (TID),
    CONSTRAINT fk_token_utilisateur
        FOREIGN KEY (UID) REFERENCES Utilisateur(UID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================
-- 8. LIVRE
-- ============================================================
-- TODO: Implement trigger to update note in Livre when a new note is added/updated in Noter
CREATE TABLE IF NOT EXISTS Livre (
    LID              INT          NOT NULL AUTO_INCREMENT,
    EID              INT          NOT NULL,  -- FK -> Editeur
    ISBN             VARCHAR(20)  NOT NULL UNIQUE, -- ISBN-13 ou ISBN-10
    nom              VARCHAR(255) NOT NULL,
    description      TEXT,
    url_couverture   VARCHAR(255),
    url_contenu      VARCHAR(255),
    note             DECIMAL(3,2),           -- attribut dérivé (AVG), nullable
    date_publication DATE NOT NULL,

    PRIMARY KEY (LID),
    CONSTRAINT fk_livre_editeur
        FOREIGN KEY (EID) REFERENCES Editeur(EID)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================
-- 9. ECRIT  (Auteur M:N Livre)
-- ============================================================
CREATE TABLE IF NOT EXISTS Ecrit (
    AID INT NOT NULL,
    LID INT NOT NULL,

    PRIMARY KEY (AID, LID),
    CONSTRAINT fk_ecrit_auteur
        FOREIGN KEY (AID) REFERENCES Auteur(AID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_ecrit_livre
        FOREIGN KEY (LID) REFERENCES Livre(LID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================
-- 10. CLASSER  (Genre M:N Livre)
-- ============================================================
CREATE TABLE IF NOT EXISTS Classer (
    GID INT NOT NULL,
    LID INT NOT NULL,

    PRIMARY KEY (GID, LID),
    CONSTRAINT fk_classer_genre
        FOREIGN KEY (GID) REFERENCES Genre(GID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_classer_livre
        FOREIGN KEY (LID) REFERENCES Livre(LID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================
-- 11. SUIT  (Utilisateur M:N Livre — avec Favoris)
-- ============================================================
CREATE TABLE IF NOT EXISTS Suit (
    UID     INT     NOT NULL,
    LID     INT     NOT NULL,
    favoris BOOLEAN NOT NULL DEFAULT FALSE,

    PRIMARY KEY (UID, LID),
    CONSTRAINT fk_suit_utilisateur
        FOREIGN KEY (UID) REFERENCES Utilisateur(UID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_suit_livre
        FOREIGN KEY (LID) REFERENCES Livre(LID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================
-- 12. CONSULTER  (Utilisateur M:N Livre — date + dernière page)
-- ============================================================
CREATE TABLE IF NOT EXISTS Consulter (
    UID                   INT      NOT NULL,
    LID                   INT      NOT NULL,
    date_consultation     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    derniere_page_consultee INT,

    PRIMARY KEY (UID, LID),
    CONSTRAINT fk_consulter_utilisateur
        FOREIGN KEY (UID) REFERENCES Utilisateur(UID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_consulter_livre
        FOREIGN KEY (LID) REFERENCES Livre(LID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================
-- 13. NOTER  (Utilisateur M:N Livre — note)
-- ============================================================
CREATE TABLE IF NOT EXISTS Noter (
    UID  INT            NOT NULL,
    LID  INT            NOT NULL,
    note DECIMAL(3,2)   NOT NULL CHECK (note BETWEEN 0 AND 5),

    PRIMARY KEY (UID, LID),
    CONSTRAINT fk_noter_utilisateur
        FOREIGN KEY (UID) REFERENCES Utilisateur(UID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_noter_livre
        FOREIGN KEY (LID) REFERENCES Livre(LID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================
-- 14. COMMENTAIRE
-- ============================================================
CREATE TABLE IF NOT EXISTS Commentaire (
    CID              INT      NOT NULL AUTO_INCREMENT,
    UID              INT      NOT NULL,
    LID              INT      NOT NULL,
    message          TEXT     NOT NULL,
    date_publication DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (CID),
    UNIQUE (UID, LID),  -- one comment per user per book
    CONSTRAINT fk_commentaire_utilisateur
        FOREIGN KEY (UID) REFERENCES Utilisateur(UID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_commentaire_livre
        FOREIGN KEY (LID) REFERENCES Livre(LID)
        ON DELETE CASCADE ON UPDATE CASCADE
);