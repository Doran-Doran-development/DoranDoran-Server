from django.test import TestCase, Client
from rest_framework import status
from .models import User

client = Client()

class Login(TestCase):

    def setUp(self):
        self.credentials = {
            "email" : "hanbin8269@gmail.com",
            "password" : "0128gksqls",
        }
        User.objects.create_user(**self.credentials)

    def test_login_success(self):
        response = client.post(
            "/auth/login", self.credentials,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_failed_with_not_exist_account(self):
        fake_credentials = {
            "email" : "gksqls0128@gmail.com",
            "password" : "0128gksqls"
        }

        response = client.post(
            "/auth/login", fake_credentials,
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_incorrect_password(self):
        fake_credentials = {
            "email" : "hanbin8269@gmail.com",
            "password" : "trashpassword"
        }

        response = client.post(
            "/auth/login", fake_credentials,
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)