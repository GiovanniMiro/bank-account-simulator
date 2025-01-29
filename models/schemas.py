#API Request validation and data serialization/deserialization

from marshmallow import Schema, fields, validates
from validators import validate_password, validate_email

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    balance = fields.Decimal(default=0.00)
    admin_permission = fields.Bool(dump_only=True)
    updated_at = fields.DateTime(dump_only=True, format="%d/%m/%Y %H:%M:%S")


    @validates("password")
    def password_validation(self, value):
        validate_password(value)
    

class UserRegisterSchema(UserSchema):
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True, format="%d/%m/%Y %H:%M:%S")

    @validates("email")
    def email_validation(self, value):
        validate_email(value)


