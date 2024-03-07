from marshmallow import Schema, fields

class BaseUserSchema(Schema):
	id = fields.Integer(dump_only=True)
	username = fields.String(required=True)
	password = fields.String(required=True, load_only=True)

class BaseContactSchema(Schema):
	id = fields.Integer(dump_only=True)
	name = fields.String(required=True)
	user_id = fields.String(required=True, load_only=True)
	phone = fields.String()
	email = fields.String()


class ContactSchema(BaseContactSchema):
	pass


class UserSchema(BaseUserSchema):
	contacts = fields.List(fields.Nested(ContactSchema()), dump_only=True)
