USE online_library;
-- ============================================================
-- TRIGGER: Update Livre.note after insert/update/delete in Noter

DELIMITER $$

DROP TRIGGER IF EXISTS trg_noter_after_insert$$
CREATE TRIGGER trg_noter_after_insert
AFTER INSERT ON Noter
FOR EACH ROW
BEGIN
    UPDATE Livre
    SET note = fn_note_moyenne(NEW.LID)
    WHERE LID = NEW.LID;
END$$

DROP TRIGGER IF EXISTS trg_noter_after_update$$
CREATE TRIGGER trg_noter_after_update
AFTER UPDATE ON Noter
FOR EACH ROW
BEGIN
    UPDATE Livre
    SET note = fn_note_moyenne(NEW.LID)
    WHERE LID = NEW.LID;
END$$


DROP TRIGGER IF EXISTS trg_noter_after_delete$$
CREATE TRIGGER trg_noter_after_delete
AFTER DELETE ON Noter
FOR EACH ROW
BEGIN
    UPDATE Livre
    SET note = fn_note_moyenne(OLD.LID)
    WHERE LID = OLD.LID;
END$$

DELIMITER ;