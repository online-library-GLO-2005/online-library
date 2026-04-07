from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)  ## Only response
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)  ## Only request
