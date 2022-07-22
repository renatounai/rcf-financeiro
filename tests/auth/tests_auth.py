from django.contrib.auth.models import User as UserModel
from django.test import TestCase

from auth import user_service
from auth.user_rest import User

APPLICATION_JSON = "application/json"


class EventTest(TestCase):

    def test_login(self):
        user_service.create_account(User(email="username@gmail.com", password="123456"))
        data = {"username": "username@gmail.com", "password": "123456"}

        response = self.client.post("/api/auth/login", data, content_type=APPLICATION_JSON)
        tokens = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(tokens["refresh"])
        self.assertIsNotNone(tokens["access"])

    def test_create_account(self):
        user = {"email": "testador@gmail.com", "password": "123456"}
        response = self.client.post("/api/users/", user, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        user_created: UserModel = UserModel.objects.get_by_natural_key("testador@gmail.com")
        self.assertIsNotNone(user_created)
