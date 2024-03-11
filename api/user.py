from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, create_access_token, get_jwt
from schema import UserSchema
from models import UserModel
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError
from db import db
from config import BLOCKLIST

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/user")
class UserList(MethodView):

    @jwt_required()
    @blp.response(status_code=200, schema=UserSchema(many=True))
    def get(self):
        users = db.session.query(UserModel).all()
        return users


@blp.route("/user/<int:user_id>")
class User(MethodView):

    @jwt_required()
    @blp.response(status_code=200, schema=UserSchema)
    def get(self, user_id):
        user = db.get_or_404(UserModel, user_id)
        return user


@blp.route("/register")
class UserRegister(MethodView):

    @blp.arguments(schema=UserSchema)
    @blp.response(status_code=201, schema=UserSchema)
    def post(self, user_data):

        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(
                http_status_code=409,
                message="There is already another user with that username",
            )
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                http_status_code=500,
                message="Something occurred while attempting to create your user. Please try again.",
            )

        return {"message": "User has been created"}, 201


@blp.route("/login")
class UserLogin(MethodView):

    @blp.arguments(schema=UserSchema)
    def post(self, user_data):

        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            return {"access_token": access_token}

        abort(
            http_status_code=401,
            message="The username and password are incorrect or invalid.",
        )


@blp.route("/logout")
class UserLogOut(MethodView):

    @jwt_required()
    def post(self):
        user = get_jwt()["jti"]
        BLOCKLIST.add(user)
        return {"message": "successfully  logged out"}, 200
