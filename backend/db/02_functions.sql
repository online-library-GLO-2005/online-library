USE online_library;

DELIMITER $$

-- ============================================================
-- 1. Get average note of a book
-- ============================================================
DROP FUNCTION IF EXISTS fn_note_moyenne$$
CREATE FUNCTION fn_note_moyenne(p_lid INT)
RETURNS DECIMAL(3,2)
READS SQL DATA
BEGIN
    DECLARE v_note DECIMAL(3,2);
    SELECT AVG(note) INTO v_note FROM Noter WHERE LID = p_lid;
    RETURN COALESCE(v_note, 0);
END$$

-- ============================================================
-- 2. Check if a user has already rated a book
-- ============================================================
DROP FUNCTION IF EXISTS fn_a_deja_note$$
CREATE FUNCTION fn_a_deja_note(p_uid INT, p_lid INT)
RETURNS BOOLEAN
READS SQL DATA
BEGIN
    DECLARE v_count INT;
    SELECT COUNT(*) INTO v_count FROM Noter WHERE UID = p_uid AND LID = p_lid;
    RETURN v_count > 0;
END$$

-- ============================================================
-- 3. Count how many books a user is following
-- ============================================================
DROP FUNCTION IF EXISTS fn_nb_livres_suivis$$
CREATE FUNCTION fn_nb_livres_suivis(p_uid INT)
RETURNS INT
READS SQL DATA
BEGIN
    DECLARE v_count INT;
    SELECT COUNT(*) INTO v_count FROM Suit WHERE UID = p_uid;
    RETURN v_count;
END$$

-- ============================================================
-- 4. Is this book in user's favourites?
-- ============================================================
DROP FUNCTION IF EXISTS fn_est_favori$$
CREATE FUNCTION fn_est_favori(p_uid INT, p_lid INT)
RETURNS BOOLEAN
READS SQL DATA
BEGIN
    DECLARE v_count INT;
    SELECT COUNT(*) INTO v_count 
    FROM Suit 
    WHERE UID = p_uid AND LID = p_lid AND favoris = TRUE;
    RETURN v_count > 0;
END$$

-- ============================================================
-- 5. How many ratings does a book have?
-- ============================================================
DROP FUNCTION IF EXISTS fn_nb_notes$$
CREATE FUNCTION fn_nb_notes(p_lid INT)
RETURNS INT
READS SQL DATA
BEGIN
    DECLARE v_count INT;
    SELECT COUNT(*) INTO v_count FROM Noter WHERE LID = p_lid;
    RETURN v_count;
END$$

DELIMITER ;