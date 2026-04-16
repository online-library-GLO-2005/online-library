from marshmallow import Schema, fields


class PublisherSchema(Schema):
    id = fields.Int(dump_only=True, data_key="id")
    name = fields.Str(required=True, data_key="name")
    description = fields.Str(allow_none=True)
