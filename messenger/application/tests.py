import json
from django.test import TestCase, Client


class FillDataBaseTest(TestCase):

    def setUp(self):
        self.Client = Client()

    def test_correct(self):
        response = self.Client.get('/fill_db/')
        self.assertEqual(response.status_code, 200)
