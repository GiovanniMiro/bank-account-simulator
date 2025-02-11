#Adicionar um decorador para verificar o status de admin_permission e assim permitir o uso de certas requisições
from flask_smorest import abort
from flask_jwt_extended import get_jwt_identity
from models.user import UserModel

def admin_required(function):
    def wrapper(*args, **kwargs):

        user_id = get_jwt_identity()

        user = UserModel.query.get(user_id)

        if not user.admin_permission:
            abort(403, message='Admin permission required.')

        return function(*args, **kwargs)
    
    return wrapper