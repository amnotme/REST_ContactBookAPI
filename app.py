from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from db import db
from config import Config
from api import ContactBluePrint, UserBluePrint


def create_app(db_url=None):
    app = Flask(__name__)

    _configure_app(app, url=None)
    _configure_db(app)
    _configure_blueprints(app)
    _configure_jwt(app)

    return app


def _configure_app(app, url=None):
    app.config.from_object(Config(db_url=url))


def _configure_db(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()


def _configure_blueprints(app):
    api = Api(app)
    api.register_blueprint(ContactBluePrint)
    api.register_blueprint(UserBluePrint)


def _configure_jwt(app):
    jwt = JWTManager(app)
