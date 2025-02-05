from flask import jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from models.db import db
from models.user import UserModel
from models.deposit import DepositModel
from models.schemas import DepositSchema
from marshmallow import ValidationError
from validators import validate_amount, validate_user
from middlewares.auth import admin_required

blp = Blueprint("Deposit", "deposits", description="Operations of deposit")

@blp.route("/deposit")
class Deposit(MethodView):

    @blp.arguments(DepositSchema)
    @jwt_required()
    def post(self, deposit_data):

        try:
            deposit = DepositModel(
                account_id = deposit_data["account_id"],
                amount = deposit_data["amount"]
            )

            validate_user(deposit.account_id)

            payee = UserModel.query.get(deposit.account_id)

            payee.balance += deposit.amount

            db.session.add(deposit)
            db.session.commit()

            return {"message": f"Successful deposit of {deposit.amount} to {payee.username}"}
        
        except ValidationError as e:
            return {"message": str(e)}, 400


@blp.route("/deposits")
class DepositList(MethodView):

    @blp.response(201, DepositSchema(many=True))
    @jwt_required()
    @admin_required
    def get(self):
        deposits = DepositModel.query.all()
        return deposits
    
@blp.route("/user/<int:user_id>/deposits")
class UserDeposits(MethodView):

    @blp.response(200, DepositSchema(many=True))
    @jwt_required()
    @admin_required
    def get(self, user_id):
        user_deposits = DepositModel.query.filter(DepositModel.account_id == user_id).all()

        serialized_deposits = DepositSchema(many=True).dump(user_deposits)

        return jsonify({"user_deposits": serialized_deposits})