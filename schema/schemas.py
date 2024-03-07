from marshmallow import Schema, fields


class BaseContactSchema(Schema):
	id = fields.Integer(dump_only=True)
	phone = fields.String()
	email = fields.String()


class ContactSchema(BaseContactSchema):
	name = fields.String(required=True)


class ContactUpdateSchema(BaseContactSchema):
	name = fields.String()
