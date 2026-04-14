from marshmallow import Schema, fields

class PublisherSchema(Schema):
    id = fields.Int(dump_only=True, data_key="EID")
    name = fields.Str(required=True, data_key="nom")
    description = fields.Str(allow_none=True)