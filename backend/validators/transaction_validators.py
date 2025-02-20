from marshmallow import ValidationError
from backend.models.user import UserModel

def validate_amount(amount: float):
      
      if amount is None:
            raise ValidationError("Amount is required.")
      
      if amount <= 0.00:
            raise ValidationError("Amount must be greater than zero.")
    
def validate_sender_balance(sender_balance: float, transaction_amount: float):
      
      if sender_balance < transaction_amount:
            raise ValidationError("Sender has insufficient balance.")