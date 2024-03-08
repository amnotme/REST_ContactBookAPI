from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt, create_access_token
from flask.views import MethodView
from models import ContactModel
from schema import ContactSchema

from sqlalchemy.exc import SQLAlchemyError
from db import db

blp = Blueprint("contact", __name__, description="Operations for a contact")


@blp.route("/contact")
class ContactList(MethodView):

    @jwt_required()
    @blp.response(status_code=200, schema=ContactSchema(many=True))
    def get(self):
        contacts = ContactModel.query.all()
        return contacts

    @jwt_required()
    @blp.arguments(schema=ContactSchema)
    @blp.response(status_code=201, schema=ContactSchema)
    def post(self, contact_data):

        contact = ContactModel(
            name=contact_data["name"],
            phone=contact_data["phone"],
            email=contact_data["email"],
            user_id=contact_data["user_id"],
        )
        try:
            db.session.add(contact)
            db.session.commit()
        except SQLAlchemyError:
            abort(http_status_code=500, message="Unable to create contact")

        return contact


@blp.route("/contact/<int:contact_id>")
class Contact(MethodView):

    @jwt_required()
    @blp.response(status_code=200, schema=ContactSchema)
    def get(self, contact_id):
        return ContactModel.query.get_or_404(
            contact_id, description=f"Contact was not found"
        )

    @jwt_required()
    @blp.arguments(schema=ContactSchema)
    @blp.response(status_code=200, schema=ContactSchema)
    def put(self, contact_data, contact_id):

        if contact := ContactModel.query.get(contact_id):
            contact.phone = contact_data.get("phone", contact.phone)
            contact.email = contact_data.get("email", contact.email)
            contact.name = contact_data.get("name", contact.name)
            contact.user_id = contact_data.get("user_id", contact.user_id)

        else:
            contact = ContactModel(
                id=contact_id,
                name=contact_data["name"],
                phone=contact_data["phone"],
                email=contact_data["email"],
                user_id=contact_data["user_id"],
            )
        try:
            db.session.add(contact)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                http_status_code=500, message="An error occurred while updating contact"
            )
        return contact

    @jwt_required()
    @blp.response(
        status_code=202,
        description="Deletes a tag if no item is tagged with it",
        example={"message": "Tag has been deleted"},
    )
    def delete(self, contact_id):

        contact = ContactModel.query.get_or_404(
            contact_id, description=f"Contact was not found"
        )

        try:
            db.session.delete(contact)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                http_status_code=500,
                message="An error occurred while attempting to deleted the contact",
            )

        return {"message": "Contact has been deleted"}, 200
