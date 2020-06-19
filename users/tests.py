from .models import User
from munch import Munch
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase


class UserLoginTestCase(APITestCase):
    url = '/api/users/login'

    def setUp(self) -> None:
        self.email = 'test@test.com'
        self.password = '1234'
        self.user = User.objects.create(email=self.email, password=self.password)

    def test_login(self):
        user = self.user
        password = self.password
        print(user, password)
        data = {'email': user.email, 'password': password}
        response = self.client.post(self.url, data=data)

        # check status code
        # check token created

