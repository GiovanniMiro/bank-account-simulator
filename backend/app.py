import os
from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from sqlalchemy import create_engine
from flask_jwt_extended import JWTManager
from .blocklist import BLOCKLIST
from .models.db import db

from .routes.user import blp as UserBlueprint
from .routes.transaction import blp as TransactionBlueprint
from .routes.deposit import blp as DepositBlueprint

def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config["API_TITLE"] = "Bank Account Simulator API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///project.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    app.config["OPENAPI_URL_PREFIX"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["API_SPEC_OPTIONS"] = {
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        }
    }

    db.init_app(app)

    migrate = Migrate(app, db)
    api = Api(app)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST


    @app.before_request
    def create_tables():

        app.before_request_funcs[None].remove(create_tables)
        db.create_all()

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(TransactionBlueprint)
    api.register_blueprint(DepositBlueprint)

    return app