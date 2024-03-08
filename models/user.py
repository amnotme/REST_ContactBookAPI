from db import db
from sqlalchemy import Column, String, Integer


class UserModel(db.Model):
    __tablename__ = "users"
    id = Column(Integer, unique=True, autoincrement=True, primary_key=True)

    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    contacts = db.relationship("ContactModel", back_populates="user", lazy="dynamic")
