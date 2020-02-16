import json
from django.test import TestCase, Client
from users.factories import *


class CreateUserTest(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.Client = Client()

    def test_correct(self):
        body1 = {
            'name': 'Vasiliy',
            'tag': '@Vasiliy',
            'bio': '',
            'password': 'Vasiliy1234'
        }
        body2 = {
            'name': 'Vasiliy',
            'tag': 'VasiliyPupkin',
            'bio': 'I\'m a manager',
            'password': 'Vasiliy1234'
        }
        response1 = self.Client.post('/users/create_user/', json.dumps(body1), content_type="application/json")
        response2 = self.Client.post('/users/create_user/', json.dumps(body2), content_type="application/json")
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_tag_exists(self):
        UserFactory.create(tag='@Vasiliy')
        body = {
            'name': 'Vasiliy',
            'tag': '@Vasiliy',
            'bio': '',
            'password': 'Vasiliy1234'
        }
        response = self.Client.post('/users/create_user/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_method_not_allowed(self):
        response = self.Client.get('/users/create_user/')
        self.assertEqual(response.status_code, 405)


class AuthTest(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.Client = Client()

    def test_correct(self):
        response = self.Client.get('/users/auth/?tag=@Tigran&password=@Tigran')
        self.assertEqual(response.status_code, 200)

    def test_no_tag(self):
        response = self.Client.get('/users/auth/?tag=@Tigran1234&password=@Tigran')
        self.assertEqual(response.status_code, 400)

    def test_wrong_password(self):
        response = self.Client.get('/users/auth/?tag=@Tigran&password=@Tigran1234')
        self.assertEqual(response.status_code, 400)

    def test_method_not_allowed(self):
        response = self.Client.post('/users/auth/?tag=@Tigran&password=@Tigran1234')
        self.assertEqual(response.status_code, 405)


class ChangePasswordTest(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.Client = Client()

    def test_correct(self):
        body = {
            'old_password': '@Tigran',
            'new_password': '@Tigran1234',
            'tag': '@Tigran'
        }

        response = self.Client.post('/users/change_password/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_no_user(self):
        body = {
            'old_password': '@Tigran',
            'new_password': '@Tigran1234',
            'tag': '@Tigran239'
        }

        response = self.Client.post('/users/change_password/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_wrong_password(self):
        body = {
            'old_password': '@Tigran239',
            'new_password': '@Tigran1234',
            'tag': '@Tigran'
        }

        response = self.Client.post('/users/change_password/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_method_not_allowed(self):
        response = self.Client.get('/users/change_password/')
        self.assertEqual(response.status_code, 405)


class FindUsersTest(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.Client = Client()

    def test_correct(self):
        response = self.Client.get('/users/find_users/?tag=@')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.json()['users'], [])
        response = self.Client.get('/users/find_users/?name=Tig')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()['users'])
        response = self.Client.get('/users/find_users/?name=jksdnfjkvnzd')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['users'], [])

    def test_method_not_allowed(self):
        response = self.Client.post('/users/find_users/?tag=@')
        self.assertEqual(response.status_code, 405)


class UserProfileTest(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.Client = Client()

    def test_correct(self):
        response = self.client.get('/users/profile/?tag=@Tigran')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()['name'])
        response = self.client.get('/users/profile/?id=1')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()['tag'])

    def test_bad_request(self):
        response = self.client.get('/users/profile/')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], 'no id or tag')

    def test_no_user(self):
        response = self.client.get('/users/profile/?tag=trew')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], 'no such user')

    def test_method_not_allowed(self):
        response = self.client.post('/users/profile/?tag=trew')
        self.assertEqual(response.status_code, 405)


class SetUserTest(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.Client = Client()

    def test_correct(self):
        body1 = {
            'name': 'Tigran239',
            'tag':  '@Tigraaaan',
            'bio': 'Happy Hummingbird',
            'old_tag': '@Tigran',
            'old_password': '@Tigran',
            'new_password': 'qwerty'
        }
        body2 = {
            'name': 'Martin239',
            'tag': '@Maaartin',
            'bio': 'Happy Hummingbird',
            'old_tag': '@Martin',
            'old_password': '',
            'new_password': ''
        }

        response1 = self.Client.post('/users/set_user/', json.dumps(body1), content_type="application/json")
        response2 = self.Client.post('/users/set_user/', json.dumps(body2), content_type="application/json")
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_not_valid_tag(self):
        body = {
            'name': 'Tigran239',
            'tag': 'Tigraaaan',
            'bio': 'Happy Hummingbird',
            'old_tag': '@Tigran',
            'old_password': '@Tigran',
            'new_password': 'qwerty'
        }

        response = self.client.post('/users/set_user/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_wrong_old_tag(self):
        body = {
            'name': 'Tigran239',
            'tag': '@Tigraaaan',
            'bio': 'Happy Hummingbird',
            'old_tag': '@Tigran1234',
            'old_password': '@Tigran',
            'new_password': 'qwerty'
        }

        response = self.client.post('/users/set_user/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_tag_exists(self):
        body = {
            'name': 'Tigran239',
            'tag': '@Martin',
            'bio': 'Happy Hummingbird',
            'old_tag': '@Tigran',
            'old_password': '@Tigran',
            'new_password': 'qwerty'
        }

        response = self.client.post('/users/set_user/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_wrong_old_password(self):
        body = {
            'name': 'Tigran239',
            'tag': '@Tigraaaan',
            'bio': 'Happy Hummingbird',
            'old_tag': '@Tigran',
            'old_password': '@Tigran1234',
            'new_password': 'qwerty'
        }

        response = self.client.post('/users/set_user/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_method_not_allowed(self):
        response = self.client.get('/users/set_user/')
        self.assertEqual(response.status_code, 405)


class ReadMessageTest(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.Client = Client()

    def test_correct(self):
        body = {
            'chat_id': 25,
            'user_id': 5,
            'message_id': 592
        }

        response = self.Client.post('/users/read_message/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_no_user(self):
        body = {
            'chat_id': 25,
            'user_id': 125,
            'message_id': 592
        }

        response = self.Client.post('/users/read_message/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_no_chat(self):
        body = {
            'chat_id': 125,
            'user_id': 5,
            'message_id': 592
        }

        response = self.Client.post('/users/read_message/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_not_a_member(self):
        body = {
            'chat_id': 25,
            'user_id': 3,
            'message_id': 592
        }

        response = self.Client.post('/users/read_message/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_no_message(self):
        body = {
            'chat_id': 25,
            'user_id': 5,
            'message_id': 2000
        }

        response = self.Client.post('/users/read_message/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_no_message_in_chat(self):
        body = {
            'chat_id': 25,
            'user_id': 5,
            'message_id': 3
        }

        response = self.Client.post('/users/read_message/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_method_not_allowed(self):
        response = self.Client.get('/users/read_message/')
        self.assertEqual(response.status_code, 405)
