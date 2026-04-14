from marshmallow import Schema, fields
from .user_schema import UserSchema


class AuthSchema(Schema):
    user = fields.Nested(UserSchema, dump_only=True)
    access_token = fields.Str(dump_only=True, data_key="token_access")
    refresh_token = fields.Str(dump_only=True, data_key="token_refresh")


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, data_key="password")


class RegisterSchema(Schema):
    name = fields.Str(required=True, data_key="name")
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, data_key="password")

    # The following would be too much for registration, we can ask for them later in the user profile setup:
    # birth_date = fields.Date(data_key="date_naissance")
    # phone = fields.Str(data_key="telephone")
    # address = fields.Str(data_key="adresse")


class RefreshSchema(Schema):
    access_token = fields.Str(required=True, data_key="token_access")
