#API Request validation and data serialization/deserialization

from marshmallow import Schema, fields, validates, ValidationError
from validators import validate_password, validate_email, validate_amount, validate_user
from models.user import UserModel


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

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class TransactionSchema(Schema):
    sender_id = fields.Int(required=True)
    receiver_id = fields.Int(required=True)
    amount = fields.Decimal(required=True)
    sent_at = fields.DateTime(dump_only=True, format="%d/%m/%Y %H:%M:%S")

    @validates("amount")
    def amount_validation(self, value):
        validate_amount(value)

class DepositSchema(Schema):
    account_id = fields.Int(required=True)
    amount = fields.Decimal(required=True)
    deposited_at = fields.DateTime(dump_only=True, format="%d/%m/%Y %H:%M:%S")

    @validates("amount")
    def amount_validation(self, value):
        validate_amount(value)