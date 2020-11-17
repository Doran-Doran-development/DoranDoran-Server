from django.test import TestCase, Client
from rest_framework import status
from room.models import Room

client = Client()

class Room(TestCase):

    def setUp(self):
        self.base_room_form = {
            "name":"class2",
            "max_team":2,
            "owner":1
        }

    def tearDown(self):
        Room.objects.all().delete()

    def test_create_room_success(self):
        room = self.base_room_form

        response = client.post('/room', room, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_room_failed_with_incorrect_form(self):
        room = self.base_room_form
        del room['name']

        response = client.post('/room',room,content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_room_failed_with_incorrect_owner(self):
        room = self.base_room_form

        room['owner'] = 0

        response = client.post('/room',room,content_type='application/json')

        self.assertEqual(reponse.status_code, status.HTTP_400_BAD_REQUEST)

