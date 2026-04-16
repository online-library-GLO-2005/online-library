USE online_library;

-- myuser is created by Docker Compose via MYSQL_USER/MYSQL_PASSWORD env vars.
-- By default, Docker grants all privileges on MYSQL_DATABASE to MYSQL_USER.
-- Here we restrict those privileges to only what the application needs.
REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'myuser'@'%';

GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE
ON online_library.* TO 'myuser'@'%';

FLUSH PRIVILEGES;

