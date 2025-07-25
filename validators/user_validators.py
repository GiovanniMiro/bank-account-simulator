from flask_smorest import abort
from marshmallow import ValidationError
from email_validator import validate_email as is_email_valid, EmailNotValidError
from werkzeug.security import check_password_hash
from models.user import UserModel
from models.db import db

def validate_user(user_id: int):
     if not UserModel.query.get(user_id):
          abort(404, "User not found.")

def validate_password(password: str):
    if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long.")
    
def validate_email_format(email: str):
    try:
        is_email_valid(email)
    except EmailNotValidError:
        raise ValidationError("Email format is not valid.")
