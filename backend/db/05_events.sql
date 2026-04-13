USE online_library;

-- ============================================================
-- EVENTS
-- ============================================================

-- Also set via Docker-compose
SET GLOBAL event_scheduler = ON;

DELIMITER $$

DROP EVENT IF EXISTS ev_purge_expired_tokens$$
CREATE EVENT IF NOT EXISTS ev_purge_expired_tokens
ON SCHEDULE EVERY 1 HOUR
DO
BEGIN
    DELETE FROM Refresh_tokens
    WHERE expires_at < NOW()
       OR revoked = TRUE;
END$$

DELIMITER ;