from models.db import db

class TransactionModel(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    sent_at = db.Column(db.DateTime, default=db.func.now())

    #A transaction has one sender
    sender = db.relationship("UserModel", back_populates="sent_transactions")

    #A transaction has one receiver 
    receiver = db.relationship("UserModel", back_populates="received_transactions")
