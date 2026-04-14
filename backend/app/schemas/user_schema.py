from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True, data_key="UID")
    name = fields.Str(required=True, data_key="nom")
    email = fields.Email(required=True, data_key="email")
    password = fields.Str(load_only=True, data_key="mot_de_passe_hash")
    birth_date = fields.Date(data_key="date_naissance")
    phone = fields.Str(data_key="telephone")
    address = fields.Str(data_key="adresse")
    created_at = fields.DateTime(dump_only=True, data_key="date_creation_compte")
