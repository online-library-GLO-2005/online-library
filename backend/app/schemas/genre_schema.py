from marshmallow import Schema, fields


class GenreSchema(Schema):
    id = fields.Int(dump_only=True, data_key="id")
    name = fields.Str(required=True, data_key="name")
