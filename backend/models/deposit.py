from models.db import db

class DepositModel(db.Model):
    __tablename__= "deposits"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    deposited_at = db.Column(db.DateTime, default=db.func.now())

    payee = db.relationship("UserModel",
                            back_populates="received_deposits",
                            foreign_keys=[account_id])