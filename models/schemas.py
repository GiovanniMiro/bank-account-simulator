from marshmallow import Schema, fields, validates, ValidationError
#Base schema class with which to define schemas.

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    balance = fields.Numeric(default=0.00)
    updated_at = fields.DateTime(dump_only=True)

    @validates("password")
    def password_validation(self, value):
        if len(value) < 6:
            raise ValidationError("Password must be at least 6 characters long.")

class UserRegisterSchema(UserSchema):
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)
    status = fields.Bool(dump_only=True)



