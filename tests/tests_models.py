import unittest
from db import db
from app import create_app
from models import *


class ModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("sqlite://:memory")
        self.app_context = self.app.app_context()  # Create an application context
        self.app_context.push()  # Push the context so the app behaves like it's handling a request
        self.client = self.app.test_client()

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

    def test_register(self):

        auth_headers = self.client.post(
            "/register", json={"username": "JD", "password": "1234"}
        )
        self.assertIsNotNone(auth_headers)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()  # Don't forget to pop the context!
