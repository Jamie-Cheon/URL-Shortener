from rest_framework.authtoken.models import Token
from .models import User
from munch import Munch
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase


class UserLoginTestCase(APITestCase):
    url = '/api/users/login'

    def setUp(self) -> None:
        self.email = 'login@test.com'
        self.password = '1234'
        self.user = User.objects.create(email=self.email)
        self.user.set_password(self.password)
        self.user.save()

    def test_without_password(self):
        response = self.client.post(self.url, {"email": self.email})
        self.assertEqual(400, response.status_code)

    def test_with_wrong_password(self):
        response = self.client.post(self.url, {"email": self.email, "password": "1111"})
        self.assertEqual(404, response.status_code)

    def test_without_email(self):
        response = self.client.post(self.url, {"password": self.password})
        self.assertEqual(400, response.status_code)

    def test_with_wrong_email(self):
        response = self.client.post(self.url, {"email": "wrong@email.com", "password": self.password})
        self.assertEqual(404, response.status_code)

    def test_with_correct_info(self):
        response = self.client.post(self.url, {"email": self.email, "password": self.password})
        self.assertEqual(200, response.status_code)

    def test_is_token_created(self):
        response = self.client.post(self.url, {"email": self.email, "password": self.password})
        self.assertTrue(response.data['token'])
