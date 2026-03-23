from extensions import ma
from marshmallow import fields

class BookCreateSchema(ma.Schema):
    title = fields.Str(required=True)
    description = fields.Str()

class BookResponseSchema(ma.Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()