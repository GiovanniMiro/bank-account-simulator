#API Request validation and data serialization/deserialization

from marshmallow import Schema, fields, validates, ValidationError
from validators import validate_password, validate_email_format, validate_amount, validate_user
from models.user import UserModel


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=False)
    password = fields.Str(required=True, load_only=True)
    balance = fields.Decimal(dump_only=True)
    admin_permission = fields.Bool(dump_only=True)
    updated_at = fields.DateTime(dump_only=True, format="%d/%m/%Y %H:%M:%S")


    @validates("password")
    def password_validation(self, value, **kwargs):
        validate_password(value)    

class UserRegisterSchema(UserSchema):
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True, format="%d/%m/%Y %H:%M:%S")

    @validates("email")
    def email_validation(self, value, **kwargs):
        validate_email_format(value)

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class TransactionSchema(Schema):
    receiver_email = fields.Email(required=True)
    amount = fields.Decimal(required=True)
    sent_at = fields.DateTime(dump_only=True, format="%d/%m/%Y %H:%M:%S")

    @validates("amount")
    def amount_validation(self, value):
        validate_amount(value)

class AdminTransactionSchema(TransactionSchema):
    sender_id = fields.Int(required=True, dump_only=True)
    receiver_id = fields.Int(required=True, dump_only=True)

class DepositSchema(Schema):
    account_email = fields.Email(required=True)
    amount = fields.Decimal(required=True)
    deposited_at = fields.DateTime(dump_only=True, format="%d/%m/%Y %H:%M:%S")

    @validates("amount")
    def amount_validation(self, value):
        validate_amount(value)
        
class AdminDepositSchema(DepositSchema):
    account_id = fields.Int(required=True, dump_only=True)

    