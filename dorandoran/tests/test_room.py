from django.test import TestCase, Client
from rest_framework import status
from room.models import Room
from account.models import User
from django.contrib.auth.hashers import make_password

import json


client = Client()

class RoomCreate(TestCase):

    def setUp(self):

        normal_user = { 
            "name" : "seojin",
            "email" : "seojin@gmail.com",
            "password" : make_password("0128gksqls"),
        }
        User.objects.create(**normal_user)

        teacher_user = { 
            "name" : "teacher",
            "email" : "teacher@gmail.com",
            "password" : make_password("0128gksqls"),
            "role" : 2
        }
        User.objects.create(**teacher_user)

        self.base_room_form = {
            "name":"class2",
            "max_team":2,
        }

        normal_user_login = {
            "email" : "seojin@gmail.com",
            "password" : "0128gksqls",
        }

        teacher_user_login = { 
            "email" : "teacher@gmail.com",
            "password" : "0128gksqls",
        }

        response = client.post(
            "/auth/login", normal_user_login,
            content_type="application/json"
        )

        self.student_token = response.json()["token"]

        response = client.post(
            "/auth/login", teacher_user_login,
            content_type="application/json"
        )

        self.teacher_token = response.json()["token"]
    def tearDown(self):
        Room.objects.all().delete()
        User.objects.all().delete()

    def test_create_room_success(self):
        response = client.post(
            '/room/', self.base_room_form, content_type='application/json',
            HTTP_AUTHORIZATION= "jwt "+ self.teacher_token
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_room_failed_with_incorrect_form(self):
        room = self.base_room_form
        del room["name"]

        response = client.post('/room/',room,content_type='application/json',HTTP_AUTHORIZATION= "jwt "+ self.teacher_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


