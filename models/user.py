from models.db import db

class UserModel(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    balance = db.Column(db.Numeric(10,2), nullable=False, default=0.00)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    admin_permission = db.Column(db.Boolean, nullable=False, default=False)

    #A user can have many sent transactions
    sent_transactions = db.relationship("TransactionModel", foreign_keys="[Transaction.sender_id]", back_populates="sender")
    
    #A user can have many received transactions
    received_transactions = db.relationship("TransactionModel", foreign_keys="[Transaction.receiver_id]", back_populates="receiver")
