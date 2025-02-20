from backend.models.db import db

class TransactionModel(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    sent_at = db.Column(db.DateTime, default=db.func.now())
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


    #A transaction has one sender
    sender = db.relationship("UserModel",
                             back_populates="sent_transactions",
                             foreign_keys=[sender_id])
    #A transaction has one receiver 
    receiver = db.relationship("UserModel",
                               back_populates="received_transactions",
                               foreign_keys=[receiver_id])
