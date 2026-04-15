from app.repositories.base_repo import BaseRepo
from app.models.token import Token
from app.models.user import User


class AuthRepo(BaseRepo):

    def find_user_by_email(self, email: str):
        query = f"""
            SELECT * FROM {User.TABLE}
            WHERE {User.Columns.EMAIL} = %s
        """
        rows = self._db.execute(query, (email,))
        return User.from_dict(rows[0]) if rows else None

    def get_user_by_id(self, uid: int):
        query = f"""
            SELECT * FROM {User.TABLE}
            WHERE {User.Columns.ID} = %s
        """
        rows = self._db.execute(query, (uid,))
        return User.from_dict(rows[0]) if rows else None

    def get_all_users(self):
        query = f"SELECT * FROM {User.TABLE}"
        rows = self._db.execute(query)
        return [User.from_dict(r) for r in rows] if rows else []

    def is_admin(self, uid: int) -> bool:
        query = f"""
            SELECT 1
            FROM {User.Admin_TABLE}
            WHERE {User.Columns.ID} = %s
        """
        rows = self._db.execute(query, (uid,))
        return bool(rows)

    def register(self, name: str, email: str, hashed_password: str):
        query = "CALL sp_inscrire_client(%s, %s, %s)"
        rows = self._db.execute(query, (name, email, hashed_password))

        # procedure returns SELECT * FROM Utilisateur
        return User.from_dict(rows[0]) if rows and rows[0] else None

    def promote_to_admin(self, uid: int):
        query = "CALL sp_promouvoir_admin(%s)"
        rows = self._db.execute(query, (uid,))

        return User.from_dict(rows[0]) if rows and rows[0] else None

    # =========================
    # Refresh token handling
    # =========================

    def store_refresh_token(self, uid: int, jti: str, token_hash: str, expires_at=None):
        query = f"""
            INSERT INTO {Token.TABLE}
            ({Token.Columns.UID},
             {Token.Columns.JTI},
             {Token.Columns.TOKEN_HASH},
             {Token.Columns.EXPIRES_AT})
            VALUES (%s, %s, %s, %s)
        """
        self._db.execute(query, (uid, jti, token_hash, expires_at))


    def get_refresh_token_by_jti(self, jti: str):
        query = f"SELECT * FROM {Token.TABLE} WHERE {Token.Columns.JTI} = %s"
        rows = self._db.execute(query, (jti,))
        return Token.from_dict(rows[0]) if rows else None

    def revoke_refresh_token(self, jti: str):
        query = f"""
            UPDATE {Token.TABLE}
            SET {Token.Columns.REVOKED} = TRUE
            WHERE {Token.Columns.JTI} = %s
        """
        self._db.execute(query, (jti,))

    def validate_refresh_token(self, jti: str):
        query = f"""
            SELECT {Token.Columns.UID}
            FROM {Token.TABLE}
            WHERE {Token.Columns.JTI} = %s
              AND {Token.Columns.REVOKED} = FALSE
              AND {Token.Columns.EXPIRES_AT} > NOW()
        """
        rows = self._db.execute(query, (jti,))
        return Token.from_dict(rows[0]) if rows else None


auth_repo = AuthRepo()
