from db import db
from sqlalchemy import Column, Integer, String


class ContactModel(db.Model):
	id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
	name = Column(String(80), nullable=False)
	phone = Column(String(20), nullable=True)
	email = Column(String(100), nullable=True)

	def __repr__(self):
		return f"Contact id: {self.id}, name: {self.name}, phone: {self.phone}, email: {self.email}"
