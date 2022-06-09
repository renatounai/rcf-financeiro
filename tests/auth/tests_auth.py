from django.contrib.auth import get_user_model
from django.test import TestCase


APPLICATION_JSON = "application/json"


class EventoTest(TestCase):

    def test_login(self):
        user_model = get_user_model()
        user = user_model.objects.create_user('username', 'username@gmail.com', '123456')
        data = {"username": user.username, "password": "123456"}

        response = self.client.post("/api/auth/login", data, content_type=APPLICATION_JSON)
        tokens = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(tokens["refresh"])
        self.assertIsNotNone(tokens["access"])

