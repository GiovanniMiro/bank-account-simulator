from flask import Flask
from routes.interface import blp as InterfaceBlueprint



def create_app():
    app = Flask(__name__)

    app.register_blueprint(InterfaceBlueprint)

    return app