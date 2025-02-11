from flask import jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.transaction import TransactionModel
from models.user import UserModel
from models.schemas import TransactionSchema, AdminTransactionSchema
from marshmallow import ValidationError
from validators import validate_user, validate_sender_balance
from middlewares.auth import admin_required
from models.db import db
from sqlalchemy import and_


blp = Blueprint("Transactions", "transaction", description="Transactions between users")

#Change transaction to only receive the receiver id and use the send id from the logged user.
@blp.route("/transaction")
class Transaction(MethodView):

    @blp.arguments(TransactionSchema)
    @jwt_required()
    def post(self, transaction_data):

        sender_id = get_jwt_identity()
        sender = UserModel.query.get(sender_id)
        receiver = UserModel.query.filter_by(email=transaction_data["receiver_email"]).first()

        if not receiver:
            abort(404, message="User not found.")

        try:
            transaction = TransactionModel(
                sender_id = sender.id,
                receiver_id = receiver.id,
                amount = transaction_data["amount"]
            )
            
            validate_sender_balance(sender.balance, transaction.amount)

            sender.balance -= transaction.amount  
            receiver.balance += transaction.amount 

            db.session.add(transaction)
            db.session.commit()

            return {"message": f"Successful transaction of {transaction.amount} to {receiver.username}"}, 200
    
        except ValidationError as e:
            return {"message": str(e)}, 400

@blp.route("/transactions")
class CurrentUserTransactions(MethodView):
    
    @blp.response(200, TransactionSchema(many=True))
    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()
        sent_transactions = TransactionModel.query.filter(TransactionModel.sender_id == user_id).all()
        received_transactions = TransactionModel.query.filter(TransactionModel.receiver_id == user_id).all()

        serialized_sent = TransactionSchema(many=True).dump(sent_transactions)
        serialized_received = TransactionSchema(many=True).dump(received_transactions)

        return jsonify({
            "sent_transactions": serialized_sent,
            "received_transactions": serialized_received
        })

@blp.route("/transaction-list")
class TransactionList(MethodView):

    @blp.response(200, AdminTransactionSchema(many=True))
    @jwt_required()
    @admin_required
    def get(self):
        transactions = TransactionModel.query.all()
        return transactions
    
@blp.route("/user/<int:user_id>/transactions")
class UserTransactions(MethodView):

    @blp.response(200, AdminTransactionSchema(many=True))
    @jwt_required()
    @admin_required
    def get(self, user_id):
        sent_transactions = TransactionModel.query.filter(TransactionModel.sender_id == user_id).all()
        received_transactions = TransactionModel.query.filter(TransactionModel.receiver_id == user_id).all()

        serialized_sent = AdminTransactionSchema(many=True).dump(sent_transactions)
        serialized_received = AdminTransactionSchema(many=True).dump(received_transactions)


        return jsonify({
            "sent_transactions": serialized_sent,
            "received_transactions": serialized_received
        })