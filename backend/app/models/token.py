class Token:
    TABLE = "Refresh_tokens"

    class Columns:
        ID = "TID"
        UID = "UID"
        JTI = "jti"
        TOKEN_HASH = "token_hash"
        EXPIRES_AT = "expires_at"
        REVOKED = "revoked"
        CREATED_AT = "created_at"

    def __init__(self, id: int, uid: int, jti: str, token_hash: str,
                 expires_at, revoked: bool, created_at=None):
        self.id = id
        self.uid = uid
        self.jti = jti
        self.token_hash = token_hash
        self.expires_at = expires_at
        self.revoked = revoked
        self.created_at = created_at

    @staticmethod
    def from_dict(data: dict):
        if not data:
            return None
        return Token(
            id=data.get(Token.Columns.ID),
            uid=data.get(Token.Columns.UID),
            jti=data.get(Token.Columns.JTI),
            token_hash=data.get(Token.Columns.TOKEN_HASH),
            expires_at=data.get(Token.Columns.EXPIRES_AT),
            revoked=bool(data.get(Token.Columns.REVOKED)),
            created_at=data.get(Token.Columns.CREATED_AT)
        )