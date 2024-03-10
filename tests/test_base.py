import unittest
from db import db
from app import create_app
import json


class TestBase(unittest.TestCase):

    test_user = "testuser"
    password = "password"
    access_token = None

    def setUp(self):
        self.app = create_app("sqlite:///:memory")
        self.app.config["JWT_SECRET_KEY"] = "secret"
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.register()
        self.access_token = self.get_access_token()

    def get_access_token(self):
        data = self.authenticate()
        authorization_headers = {
            "Authorization": f"Bearer {self.decode_string(data).get('access_token')}"
        }
        return authorization_headers

    def register(self, user=test_user, password=password):
        message = self.client.post(
            "/register",
            json={"username": user, "password": password},
        )
        return message

    def decode_string(self, byte_str):
        return json.loads(byte_str.data.decode())

    def authenticate(self, user=test_user, password=password):
        response = self.client.post(
            "/login", json={"username": user, "password": password}
        )
        return response

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
