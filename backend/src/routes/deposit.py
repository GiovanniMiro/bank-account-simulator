from flask import jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db import db
from models.user import UserModel
from models.deposit import DepositModel
from models.schemas import DepositSchema, AdminDepositSchema
from marshmallow import ValidationError
from validators import validate_amount, validate_user
from middlewares.auth import admin_required

blp = Blueprint("Deposit", "deposits", description="Operations of deposit")

@blp.route("/deposit")
class Deposit(MethodView):

    @blp.arguments(DepositSchema)
    @jwt_required()
    def post(self, deposit_data):
        
        payee = UserModel.query.filter_by(email=deposit_data["account_email"]).first()

        if not payee:
            abort(404, message="User not found.")

        try:
            deposit = DepositModel(
                account_id = payee.id,
                amount = deposit_data["amount"]
            )

            payee.balance += deposit.amount

            db.session.add(deposit)
            db.session.commit()

            return {"message": f"Successful deposit of {deposit.amount} to {payee.username}"}
        
        except ValidationError as e:
            return {"message": str(e)}, 400

@blp.route("/deposits")
class CurrentUserDeposits(MethodView):

    @blp.response(201, DepositSchema(many=True))
    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()
        user_deposits = DepositModel.query.filter(DepositModel.account_id == user_id).all()
        serialized_deposits = DepositSchema(many=True).dump(user_deposits)

        return jsonify({"deposits": serialized_deposits})

@blp.route("/deposit-list")
class DepositList(MethodView):

    @blp.response(201, AdminDepositSchema(many=True))
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