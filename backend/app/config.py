import os
import ast
from datetime import timedelta
from flask.json.provider import DefaultJSONProvider


class Config:
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    DefaultJSONProvider.sort_keys = False

    # Parses and transforms in list
    CORS_ORIGINS = ast.literal_eval(os.getenv("CORS_ORIGINS", "[]"))

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # Try to get .env var, if null, use default=15
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", 15))
    )
    # Try to get .env var, if null, use default=7
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 7))
    )
