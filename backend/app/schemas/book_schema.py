from marshmallow import Schema, fields

from app.schemas.author_schema import AuthorSchema
from app.schemas.genre_schema import GenreSchema


class BookSchema(Schema):
    id = fields.Int(dump_only=True, data_key="LID") # dump_only car auto-increment
    eid = fields.Int(required=True)
    isbn = fields.Str(required=True)
    title = fields.Str(required=True, data_key="nom")
    description = fields.Str()
    cover_url = fields.Str(data_key="url_couverture")
    content_url = fields.Str(data_key="url_contenu")
    rating = fields.Float(dump_only=True, data_key="note") # Calculé par trigger SQL
    pub_date = fields.Date(required=True, data_key="date_publication")
    authors = fields.List(fields.Nested(AuthorSchema), dump_only=True)
    genres = fields.List(fields.Nested(GenreSchema), dump_only=True)