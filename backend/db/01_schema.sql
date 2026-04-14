-- This is done by Docker-compose. 
-- CREATE DATABASE IF NOT EXISTS online_library;
USE online_library;

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

CREATE INDEX idx_auteur_nom ON Auteur (nom);

-- ============================================================
-- 3. EDITEUR
-- ============================================================
CREATE TABLE IF NOT EXISTS Editeur (
    EID         INT          NOT NULL AUTO_INCREMENT,
    nom         VARCHAR(100) NOT NULL UNIQUE,  -- publishers should have unique names
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

CREATE INDEX idx_utilisateur_nom ON Utilisateur (nom);

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
CREATE TABLE IF NOT EXISTS Refresh_tokens (
    TID         INT          NOT NULL AUTO_INCREMENT,
    UID         INT          NOT NULL,
    jti         VARCHAR(255) NOT NULL UNIQUE, -- JWT ID
    token_hash  VARCHAR(255) NOT NULL,
    expires_at  DATETIME     NOT NULL,
    revoked     BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (TID),
    CONSTRAINT fk_token_utilisateur
        FOREIGN KEY (UID) REFERENCES Utilisateur(UID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Required for the FK relationship (MySQL needs an index on the FK column).
-- Also used when fetching all tokens for a given user (e.g. logout-all).
CREATE INDEX idx_refresh_tokens_uid ON Refresh_tokens (UID);

-- Speeds up token validation: WHERE jti = ? AND revoked = FALSE AND expires_at > NOW()
CREATE INDEX idx_refresh_token_validation ON Refresh_tokens (jti, revoked, expires_at);

-- Useful for the TODO cleanup trigger / scheduled purge job: WHERE expires_at < NOW()
CREATE INDEX idx_refresh_tokens_expires ON Refresh_tokens (expires_at);

-- ============================================================
-- 8. LIVRE
-- ============================================================
CREATE TABLE IF NOT EXISTS Livre (
    LID              INT          NOT NULL AUTO_INCREMENT,
    EID              INT          NOT NULL,  -- FK -> Editeur
    ISBN             VARCHAR(20)  NOT NULL UNIQUE, -- ISBN-13 ou ISBN-10
    nom              VARCHAR(255) NOT NULL,
    description      TEXT,
    url_couverture   VARCHAR(255),
    url_contenu      VARCHAR(255),
    note             DECIMAL(3,2),           -- attribut dérivé (AVG), nullable updated on trigger
    date_publication DATE NOT NULL,

    PRIMARY KEY (LID),
    CONSTRAINT fk_livre_editeur
        FOREIGN KEY (EID) REFERENCES Editeur(EID)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Required for the FK: JOIN Livre ON Livre.EID = Editeur.EID.
CREATE INDEX idx_livre_eid ON Livre (EID);

-- Speeds up title search (e.g. catalog search bar).
CREATE INDEX idx_livre_nom ON Livre (nom);

-- Useful for sorting or filtering by publication date or top-rated books.
CREATE INDEX idx_livre_date_publication ON Livre (date_publication);
CREATE INDEX idx_livre_note ON Livre (note);

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

-- The composite PK (AID, LID) already indexes the AID-first direction.
-- We need the reverse direction for: "who are the authors of book Y?"
CREATE INDEX idx_ecrit_lid ON Ecrit (LID);

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

-- Covers the reverse: "what genres does book Y belong to?"
CREATE INDEX idx_classer_lid ON Classer (LID);

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

-- Covers: "which users follow book Y?"
CREATE INDEX idx_suit_lid ON Suit (LID);

-- Covers: "show me only my favourites" — WHERE UID = ? AND favoris = TRUE
CREATE INDEX idx_suit_uid_favoris ON Suit (UID, favoris);

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

-- Covers: "which users consulted book Y?"
CREATE INDEX idx_consulter_lid ON Consulter (LID);

-- Covers: "recently read books for user X" — ORDER BY date_consultation DESC
CREATE INDEX idx_consulter_uid_date ON Consulter (UID, date_consultation);

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

-- Required for the TODO trigger: AVG(note) WHERE LID = ?
-- Also covers FK enforcement on LID.
CREATE INDEX idx_noter_lid ON Noter (LID);

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

-- The UNIQUE(UID, LID) index covers UID-first lookups ("all comments by user X").
-- We add LID-first for the book page: "all comments on book Y".
CREATE INDEX idx_commentaire_lid ON Commentaire (LID);

-- Covers: ORDER BY date_publication DESC on a book's comment section.
CREATE INDEX idx_commentaire_date ON Commentaire (date_publication);