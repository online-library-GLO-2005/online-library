from marshmallow import Schema, fields

from app.schemas.author_schema import AuthorSchema
from app.schemas.genre_schema import GenreSchema


class BookSchema(Schema):
    id = fields.Int(dump_only=True, data_key="id")  # dump_only car auto-increment
    eid = fields.Int(required=True)
    isbn = fields.Str(required=True)
    title = fields.Str(required=True, data_key="title")
    description = fields.Str()
    cover_url = fields.Str(data_key="cover_url")
    content_url = fields.Str(data_key="content_url")
    rating = fields.Float(dump_only=True, data_key="rating")  # Calculé par trigger SQL
    pub_date = fields.Date(required=True, data_key="pub_date")
    authors = fields.List(fields.Nested(AuthorSchema), dump_only=True)
    genres = fields.List(fields.Nested(GenreSchema), dump_only=True)
