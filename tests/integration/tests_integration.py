from tests import TestBase


class IntegrationTestsCase(TestBase):

    def _mock_contact_info(self):
        return [
            {
                "name": "name1",
                "phone": "1234567890",
                "email": "name1@yes.com",
                "user_id": "1",
            },
            {
                "name": "name2",
                "phone": "1234567890",
                "email": "name2@yes.com",
                "user_id": "1",
            },
            {
                "name": "name3",
                "phone": "1234567890",
                "email": "name3@yes.com",
                "user_id": "1",
            },
        ]

    def test_get_users_endpoint(self):
        response = self.client.get("/user", headers=self.access_token)
        self.assertIsNotNone(response)
        self.assertEqual(first=200, second=response.status_code)

        data = self.decode_string(response)
        self.assertEqual(first=1, second=data[0]["id"])
        self.assertEqual(first=[], second=data[0]["contacts"])
        self.assertEqual(first="testuser", second=data[0]["username"])

    def test_create_new_user_endpoint(self):
        test_user = "testuser2"
        test_pass = "5678"
        response = self.client.post(
            "/register", json={"username": test_user, "password": test_pass}
        )
        self.assertEqual(first=201, second=response.status_code)

    def test_get_users_endpoint_unauthorized_user(self):
        authentication = self.authenticate(user="fakeuser", password="fakepassword")

        self.assertIsNotNone(authentication)
        self.assertEqual(first=401, second=authentication.status_code)

    def test_get_user_by_id_endpoint(self):
        response = self.client.get("/user/1", headers=self.access_token)
        self.assertIsNotNone(response)
        self.assertEqual(first=200, second=response.status_code)

        data = self.decode_string(response)
        self.assertEqual(first=1, second=data["id"])
        self.assertEqual(first=[], second=data["contacts"])
        self.assertEqual(first="testuser", second=data["username"])

    def test_get_user_by_id_not_found_endpoint(self):
        response = self.client.get("/user/20", headers=self.access_token)
        self.assertIsNotNone(response)
        self.assertEqual(first=404, second=response.status_code)

    def test_contacts_endpoint(self):
        def create_contacts():
            for idx, contact in enumerate(self._mock_contact_info()):
                response = self.client.post(
                    "/contact", headers=self.access_token, json=contact
                )
                self.assertEqual(first=201, second=response.status_code)
                self.assertEqual(first=f"name{idx+1}", second=response.json["name"])
                self.assertEqual(
                    first=f"name{idx+1}@yes.com", second=response.json["email"]
                )
                self.assertEqual(first=(idx + 1), second=response.json["id"])

        def get_contacts():
            response = self.client.get("/contact", headers=self.access_token)
            self.assertEqual(first=200, second=response.status_code)
            self.assertEqual(first=3, second=len(response.json))

        create_contacts()
        get_contacts()

    def test_contact_by_id_endpoint(self):

        def create_contact():
            contact = self._mock_contact_info()[0]

            response = self.client.post(
                "/contact", headers=self.access_token, json=contact
            )
            self.assertEqual(first=201, second=response.status_code)
            self.assertEqual(first="name1", second=response.json["name"])
            self.assertEqual(first="name1@yes.com", second=response.json["email"])
            self.assertEqual(first=1, second=response.json["id"])

        def update_contact():
            response = self.client.put(
                "/contact/1",
                headers=self.access_token,
                json={
                    "name": "name10",
                    "email": "name10@yes.com",
                    "phone": "0987654321",
                    "user_id": "1",
                },
            )

            self.assertEqual(first=200, second=response.status_code)
            self.assertEqual(first="name10", second=response.json["name"])
            self.assertEqual(first="name10@yes.com", second=response.json["email"])
            self.assertEqual(first="0987654321", second=response.json["phone"])

        def delete_contact():
            response = self.client.delete("/contact/1", headers=self.access_token)
            self.assertEqual(first=200, second=response.status_code)

        create_contact()
        update_contact()
        delete_contact()
