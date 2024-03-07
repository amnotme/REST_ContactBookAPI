from db import db
from sqlalchemy import Column, Integer, String, ForeignKey


class ContactModel(db.Model):
	__tablename__ = "contacts"
	id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
	name = Column(String(80), nullable=False)
	phone = Column(String(20), nullable=True)
	email = Column(String(100), nullable=True)
	user_id = Column(Integer, ForeignKey("users.id"), unique=False, nullable=False)

	user = db.relationship("UserModel", back_populates="contacts")

	def __repr__(self):
		return f"Contact id: {self.id}, name: {self.name}, phone: {self.phone}, email: {self.email}"
