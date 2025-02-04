from flask_smorest import Blueprint, abort
from flask.views import MethodView
from models.user import UserModel
from models.schemas import UserRegisterSchema, UserLoginSchema, UserSchema
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token
from sqlalchemy import or_
from models.db import db

blp = Blueprint("Users", "user", description="Operations on the user")

@blp.route("/register")
class UserRegister(MethodView):
#Using MethodView allows the get or post method to handle GET or POST requests directly,
#making it an alternative to using @blp.get or @blp.post.
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):

        #Move it to the validators module
        if UserModel.query.filter(
            or_(
                UserModel.username == user_data["username"],
                UserModel.email == user_data["email"]
            )
        ).first():
            abort(409, "A user with this username or email already exists.")

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=generate_password_hash(user_data["password"])
        )

        db.session.add(user)
        db.session.commit()

        return {"message": "User successfully created."}, 200

@blp.route("/login")
class UserLogin(MethodView):

    @blp.arguments(UserLoginSchema)
    def post(self, user_data):

        user = UserModel.query.filter_by(email=user_data["email"]).first()

        if not user or not user.check_password(user_data["password"]):
            abort(401, message="Invalid email or password.")

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        
        return {"access_token": access_token, "refresh_token": refresh_token}
        

#Make it only visible for admins    
@blp.route("/users")
class UsersList(MethodView):
    @blp.response(201, UserSchema(many=True))
    @jwt_required()
    def get(self):
        users = UserModel.query.all()
        return users

#Make it only visible for admins
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    @jwt_required()
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200

