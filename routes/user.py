from flask_smorest import Blueprint, abort
from flask.views import MethodView
from models.user import User
from passlib.hash import pbkdf2_sha256
from models.schemas import UserRegisterSchema, UserSchema
from sqlalchemy import or_
from models.db import db

blp = Blueprint("Users", "user", description="Operations on the user")

@blp.route("/register")
def UserRegister(MethodView):
#Using MethodView allows the get or post method to handle GET or POST requests directly,
#making it an alternative to using @blp.get or @blp.post.
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if User.query.filter(
            or_(
                User.username == user_data["username"],
                User.email == user_data["email"]
            )
        ).first():
            abort(409, "A user with this username or email already exists.")

        user = User(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        db.session.add(user)
        db.session.commit()

        return {"message": "User successfully created."}, 200