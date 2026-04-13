USE online_library;

DELIMITER $$

-- ============================================================
-- 1. Register a new client
-- ============================================================
DROP PROCEDURE IF EXISTS sp_inscrire_client$$
CREATE PROCEDURE sp_inscrire_client(
    IN p_nom      VARCHAR(100),
    IN p_email    VARCHAR(255),
    IN p_password VARCHAR(255)
)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Utilisateur WHERE email = p_email) THEN
        INSERT INTO Utilisateur (nom, email, mot_de_passe_hash)
        VALUES (p_nom, p_email, p_password);

        INSERT INTO Client (UID) VALUES (LAST_INSERT_ID());

        SELECT * FROM Utilisateur WHERE UID = LAST_INSERT_ID();
    ELSE
        SELECT NULL; -- duplicate
    END IF;
END$$

-- ============================================================
-- 2. Create an admin directly
-- ============================================================
DROP PROCEDURE IF EXISTS sp_creer_admin$$
CREATE PROCEDURE sp_creer_admin(
    IN p_nom      VARCHAR(100),
    IN p_email    VARCHAR(255),
    IN p_password VARCHAR(255)
)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Utilisateur WHERE email = p_email) THEN
        INSERT INTO Utilisateur (nom, email, mot_de_passe_hash)
        VALUES (p_nom, p_email, p_password);

        INSERT INTO Administrateur (UID) VALUES (LAST_INSERT_ID());

        SELECT * FROM Utilisateur WHERE UID = LAST_INSERT_ID();
    ELSE
        SELECT NULL; -- duplicate
    END IF;
END$$

-- ============================================================
-- 3. Promote a client to admin
-- ============================================================
DROP PROCEDURE IF EXISTS sp_promouvoir_admin$$
CREATE PROCEDURE sp_promouvoir_admin(
    IN p_uid INT
)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Utilisateur WHERE UID = p_uid) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Utilisateur introuvable';
    ELSEIF EXISTS (SELECT 1 FROM Administrateur WHERE UID = p_uid) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Utilisateur est deja administrateur';
    ELSE
        DELETE FROM Client WHERE UID = p_uid;
        INSERT INTO Administrateur (UID) VALUES (p_uid);

        SELECT * FROM Utilisateur WHERE UID = p_uid;
    END IF;
END$$

-- ============================================================
-- 4. Add a rating
-- ============================================================
DROP PROCEDURE IF EXISTS sp_noter_livre$$
CREATE PROCEDURE sp_noter_livre(
    IN p_uid  INT,
    IN p_lid  INT,
    IN p_note DECIMAL(3,2)
)
BEGIN
    IF fn_a_deja_note(p_uid, p_lid) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Utilisateur a deja note ce livre';
    ELSE
        INSERT INTO Noter (UID, LID, note) VALUES (p_uid, p_lid, p_note);

        SELECT * FROM Noter WHERE UID = p_uid AND LID = p_lid;
    END IF;
END$$

-- ============================================================
-- 5. Toggle a book as favourite
-- ============================================================
DROP PROCEDURE IF EXISTS sp_toggle_favori$$
CREATE PROCEDURE sp_toggle_favori(
    IN p_uid INT,
    IN p_lid INT
)
BEGIN
    IF EXISTS (SELECT 1 FROM Suit WHERE UID = p_uid AND LID = p_lid) THEN
        UPDATE Suit
        SET favoris = NOT favoris
        WHERE UID = p_uid AND LID = p_lid;
    ELSE
        INSERT INTO Suit (UID, LID, favoris) VALUES (p_uid, p_lid, TRUE);
    END IF;

    -- Always return current state
    SELECT * FROM Suit WHERE UID = p_uid AND LID = p_lid;
END$$

-- ============================================================
-- 6. Revoke all tokens of a user
-- ============================================================
DROP PROCEDURE IF EXISTS sp_revoquer_tokens$$
CREATE PROCEDURE sp_revoquer_tokens(
    IN p_uid INT
)
BEGIN
    UPDATE Refresh_tokens
    SET revoked = TRUE
    WHERE UID = p_uid;

    -- Return number of tokens revoked
    SELECT ROW_COUNT() AS tokens_revoques;
END$$

-- ============================================================
-- 7. Update reading progress
-- ============================================================
DROP PROCEDURE IF EXISTS sp_mettre_a_jour_lecture$$
CREATE PROCEDURE sp_mettre_a_jour_lecture(
    IN p_uid  INT,
    IN p_lid  INT,
    IN p_page INT
)
BEGIN
    INSERT INTO Consulter (UID, LID, date_consultation, derniere_page_consultee)
        VALUES (p_uid, p_lid, NOW(), p_page)
    ON DUPLICATE KEY UPDATE
        date_consultation       = NOW(),
        derniere_page_consultee = p_page;

    SELECT * FROM Consulter WHERE UID = p_uid AND LID = p_lid;
END$$

DELIMITER ;