from flask import Flask
from routes.interface import blp as InterfaceBlueprint
from models.db import db



def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    db.init_app(app)

    app.register_blueprint(InterfaceBlueprint)

    return app