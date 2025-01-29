from marshmallow import ValidationError
from email_validator import validate_email as is_email_valid

def validate_password(password: str):
    if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long.")
    
def validate_email(email: str):
    if not is_email_valid(email):
         raise ValidationError("Email format is not valid.")