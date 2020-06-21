from rest_framework.test import APITestCase
from munch import Munch
from model_bakery import baker
from users.models import User
from .models import Link


class LinkTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = baker.make(User)
        self.links = baker.make(Link, _quantity=3, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_links_list(self):
        url = '/api/urls'
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        for res, link in zip(response.data['results'], self.links[::-1]):
            self.assertEqual(res['id'], link.id)
            self.assertEqual(res['origin_url'], link.origin_url)
            self.assertEqual(res['owner'], link.owner.email)

    def test_link_create(self):
        url = '/api/urls'
        data = {"origin_url": "http://www.google.com", "owner": self.user}
        response = self.client.post(url, data=data)
        self.assertEqual(201, response.status_code)

        res = Munch(response.data)
        self.assertTrue(res.id)
        self.assertEqual(res.origin_url, data['origin_url'])
        self.assertEqual(res.owner, data['owner'].email)

    def test_link_retrieve(self):
        url = f'/api/urls/{self.links[0].id}'
        link = self.links[0]
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        res = Munch(response.data)
        self.assertTrue(res.id)
        self.assertEqual(res.id, link.id)
        self.assertEqual(res.short_url, link.short_url)

    def test_link_update(self):
        url = f'/api/urls/{self.links[0].id}'
        data = {"origin_url": "http://www.update.com"}
        response = self.client.put(url, data=data)

        self.assertEqual(200, response.status_code)

        res = Munch(response.data)
        self.assertEqual(res.origin_url, data['origin_url'])

    def test_link_delete(self):
        url = f'/api/urls/{self.links[0].id}'
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
        self.assertFalse(Link.objects.filter(id=self.links[0].id).exists())
