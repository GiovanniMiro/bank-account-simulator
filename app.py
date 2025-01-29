import os

from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate

from models.db import db

from routes.interface import blp as InterfaceBlueprint
from routes.user import blp as UserBlueprint

def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config["API_TITLE"] = "Bank Account Simulator API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///project.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    migrate = Migrate(app, db)

    api = Api(app)

    @app.before_request
    def create_tables():

        app.before_request_funcs[None].remove(create_tables)
        db.create_all()

    api.register_blueprint(InterfaceBlueprint)
    api.register_blueprint(UserBlueprint)

    return app