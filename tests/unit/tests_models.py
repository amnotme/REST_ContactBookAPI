from db import db
from models import *
from tests import TestBase


class ModelTestCase(TestBase):

    def test_new_user(self):
        user = UserModel(username="JD", password="1234")
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, "JD")

    def test_new_contact(self):
        contact = ContactModel(
            name="John Doe",
            phone="1234567890",
            email="johndoe@example.com",
            user_id="1",
        )
        db.session.add(contact)
        db.session.commit()
        self.assertIsNotNone(contact.id)
        self.assertEqual(contact.name, "John Doe")
