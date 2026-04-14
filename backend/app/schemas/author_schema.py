from marshmallow import Schema, fields

class AuthorSchema(Schema):
    id = fields.Int(dump_only=True, data_key="AID")
    name = fields.Str(required=True, data_key="nom")
    description = fields.Str(allow_none=True)
    photo_url = fields.Str(allow_none=True, data_key="url_photo")