from marshmallow import Schema, fields


class CommentSchema(Schema):
    id = fields.Int()
    uid = fields.Int()
    lid = fields.Int()
    message = fields.Str()
    date_publication = fields.DateTime()
    user_name = fields.Str(dump_only=True)
