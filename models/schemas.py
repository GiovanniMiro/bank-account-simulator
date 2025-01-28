from marshmallow import Schema, fields
#Base schema class with which to define schemas.

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()