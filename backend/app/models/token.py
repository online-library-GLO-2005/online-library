class Token:
    TABLE = "Refresh_tokens"

    class Columns:
        TID = "TID"
        UID = "UID"
        JTI = "jti"
        TOKEN_HASH = "token_hash"
        EXPIRES_AT = "expires_at"
        REVOKED = "revoked"
        CREATED_AT = "created_at"
