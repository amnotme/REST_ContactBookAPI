from tests import TestBase


class IntegrationTestsCase(TestBase):

    def test_user_endpoint(self):
        response = self.client.get("/user", headers=self.access_token)
        self.assertIsNotNone(response)
        self.assertEqual(first=200, second=response.status_code)

        data = self.decode_string(response)
        self.assertEqual(first=1, second=data[0]["id"])
        self.assertEqual(first=[], second=data[0]["contacts"])
        self.assertEqual(first="testuser", second=data[0]["username"])

    def test_user_endpoint_unauthorized_user(self):
        authentication = self.authenticate(user="fakeuser", password="fakepassword")

        self.assertIsNotNone(authentication)
        self.assertEqual(first=401, second=authentication.status_code)
