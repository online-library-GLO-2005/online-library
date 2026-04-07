from marshmallow import Schema, fields


class BookSchema(Schema):
    id = fields.Int(dump_only=True)  # returned by API, not required on input
    title = fields.Str(required=True)  # must be provided on input
    description = fields.Str()
