from flask_smorest import Blueprint, abort
from flask.views import MethodView
from models.transaction import TransactionModel
from models.user import UserModel
from models.schemas import TransactionSchema
from marshmallow import ValidationError
from validators import validate_sender_balance
from models.db import db
from sqlalchemy import and_


blp = Blueprint("Transactions", "transaction", description="Transactions between users")

@blp.route("/transaction")
class Transaction(MethodView):
    @blp.arguments(TransactionSchema)
    def post(self, transaction_data):
        
        try:
            transaction = TransactionModel(
                sender_id = transaction_data["sender_id"],
                receiver_id = transaction_data["receiver_id"],
                amount = transaction_data["amount"]
            )

            sender = UserModel.query.get(transaction.sender_id)
            receiver = UserModel.query.get(transaction.receiver_id)

            validate_sender_balance(sender.balance, transaction.amount)

            sender.balance -= transaction.amount  
            receiver.balance += transaction.amount 

            db.session.add(transaction)
            db.session.commit()

            return {"message": f"Successful transaction of {transaction.amount} to {receiver.username}"}, 200
    
        except ValidationError as e:
            return {"message": str(e)}, 400