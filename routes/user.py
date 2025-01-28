from flask_smorest import Blueprint
from flask.views import MethodView

blp = Blueprint("Users", "user", description="Operations on the user")

@blp.route("/register")
def UserRegister(MethodView):
#Using MethodView allows the get or post method to handle GET or POST requests directly,
#making it an alternative to using @blp.get or @blp.post.
    def post(self, user_data):