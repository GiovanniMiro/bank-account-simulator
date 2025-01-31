from flask_smorest import Blueprint
from flask.views import MethodView
from models.db import db
from models.user import UserModel
from models.deposit import DepositModel
from models.schemas import DepositSchema

blp = Blueprint("Deposit", "deposits", description="Operations of deposit")

@blp.route("/deposit")
class Deposit(MethodView):

    @blp.arguments(DepositSchema)
    def post(self, deposit_data):

        deposit = DepositModel(
            account_id = deposit_data["account_id"],
            amount = deposit_data["amount"]
        )

        payee = UserModel.query.get(deposit.account_id)

        payee.balance += deposit.amount

        db.session.add(deposit)
        db.session.commit()

        return {"message": f"Successful deposit of {deposit.amount} to {payee.username}"}
