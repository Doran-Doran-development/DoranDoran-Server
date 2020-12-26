from django.test import TestCase, Client
from rest_framework import status
from account.models import User
from django.contrib.auth.hashers import make_password


client = Client()


class Login(TestCase):

    def setUp(self):
        self.credentials = {
            "email" : "hanbin8269@gmail.com",
            "password" : "0128gksqls",
        }
        exist_user = {
            "email" : "hanbin8269@gmail.com",
            "password" : make_password("0128gksqls")
        }
        User.objects.create(**exist_user)

    def tearDown(self):
        User.objects.all().delete()

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

class SignUp(TestCase):
    
    def setUp(self):
        self.base_user_form = { # 기본 유저 폼
            "name" : "habi",
            "email" : "gksqls0128@gmail.com",
            "password" : "0128gksqls"
        }
        self.exist_user = { # 테스트를 위해 DB에 이미 존재할 계정 폼
            "name" : "hanbin",
            "email" : "hanbin8269@gmail.com",
            "password" : "0128gksqls",
        }
        User.objects.create(**self.exist_user)
    
    def tearDown(self):
        User.objects.all().delete()

    # 회원가입 성공
    def test_sign_up_success(self):
        user = self.base_user_form

        response = client.post('/auth/sign-up', user, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # 성공 - username에 한글 넣었을때
    def test_sign_up_success_with_korean_username(self):
        user = self.base_user_form
        user['name'] = "정한빈"

        response = client.post('/auth/sign-up', user, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # 실패 - email 폼에 안맞을때
    def test_sign_up_failed_with_incorrect_email_form(self):
        user = self.base_user_form
        user['email'] = "hanbin.com"

        response = client.post('/auth/sign-up', user, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 실패 - 잘못된 폼
    def test_sign_up_falied_with_incorrect_form(self):
        user = self.base_user_form
        del user['name']

        response = client.post('/auth/sign-up', user, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # 실패 - 존재하는 이메일
    def test_sign_up_failed_with_exist_email(self):
        user = self.exist_user

        response = client.post('/auth/sign-up', user, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
