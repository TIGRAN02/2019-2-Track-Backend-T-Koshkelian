import json

from django.test import TestCase, Client
from mock import patch

from chats.factories import *


class CreateChatTest(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.Client = Client()

    def test_correct(self):
        body1 = {
            'name': 'Hi',
            'tag': '@Hi',
            'bio': 'Hi',
            'creator': 4,
            'members': '@Michael @Martin @Tigran',
            'is_channel': False
        }
        body2 = {
            'name': 'Hey',
            'tag': '@Hey',
            'bio': 'Hey',
            'creator': 4,
            'members': '@Michael',
            'is_channel': False
        }
        response1 = self.Client.post('/chats/create_chat/', json.dumps(body1), content_type="application/json")
        response2 = self.Client.post('/chats/create_chat/', json.dumps(body2), content_type="application/json")
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_tag_exists(self):
        PersonalChatFactory.create(tag='@Hi')
        body = {
            'name': 'Hi',
            'tag': '@Hi',
            'bio': 'Hi',
            'creator': 4,
            'members': '@Michael @Martin @Tigran',
            'is_channel': False
        }
        response = self.Client.post('/chats/create_chat/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_no_user(self):
        body1 = {
            'name': 'Hi',
            'tag': '@Hi',
            'bio': 'Hi',
            'creator': 120,
            'members': '@Michael @Martin @Tigran',
            'is_channel': False
        }
        body2 = {
            'name': 'Hi',
            'tag': '@Hi',
            'bio': 'Hi',
            'creator': 4,
            'members': '@sjkfnvsjklgn',
            'is_channel': False
        }
        response1 = self.Client.post('/chats/create_chat/', json.dumps(body1), content_type="application/json")
        response2 = self.Client.post('/chats/create_chat/', json.dumps(body2), content_type="application/json")
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response2.status_code, 400)

    def test_empty_members(self):
        body = {
            'name': 'Hi',
            'tag': '@Hi',
            'bio': 'Hi',
            'creator': 4,
            'is_channel': False
        }
        response = self.Client.post('/chats/create_chat/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_invalid_field(self):
        body = {
            'name': 'Hisjngjkbnjkfnbkjnfgbjndfgkjbnskjfnvbjknsfjknvbksjfgnbkjnfgjkbnjkfgnbjkndfgjk',
            'tag': '@Hi',
            'bio': 'Hi',
            'creator': 4,
            'members': '@Michael @Martin @Tigran',
            'is_channel': False
        }
        response = self.Client.post('/chats/create_chat/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_changes_tag(self):
        body = {
            'name': 'asdfghjklqwerty890p',
            'tag': 'Hi Hi',
            'bio': 'Hi',
            'creator': 4,
            'members': '@Michael @Martin @Tigran',
            'is_channel': False
        }
        response = self.Client.post('/chats/create_chat/', json.dumps(body), content_type="application/json")
        self.assertNotEqual(Chat.objects.get(name='asdfghjklqwerty890p').tag, 'Hi Hi')

    def test_method_not_allowed(self):
        response = self.Client.get('/chats/create_chat/')
        self.assertEqual(response.status_code, 405)


class SendMessageTest(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.Client = Client()

    def test_correct(self):
        body1 = {
            'chat_tag': '@group_5',
            'user_id': 5,
            'type': 'text',
            'content': 'Hello',
        }
        body2 = {
            'chat_tag': '@group_5',
            'user_id': 5,
            'type': 'image',
            'url': '123',
        }
        response1 = self.Client.post('/chats/send_message/', json.dumps(body1), content_type="application/json")
        response2 = self.Client.post('/chats/send_message/', json.dumps(body2), content_type="application/json")
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_no_chat(self):
        body = {
            'chat_tag': '@group_223442323',
            'user_id': 5,
            'type': 'text',
            'content': 'Hello',
        }
        response = self.Client.post('/chats/send_message/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_no_user(self):
        body = {
            'chat_tag': '@group_5',
            'user_id': 4567,
            'type': 'text',
            'content': 'Hello',
        }
        response = self.Client.post('/chats/send_message/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_empty_message(self):
        body = {
            'chat_tag': '@group_5',
            'user_id': 5,
            'type': 'text',
        }
        response = self.Client.post('/chats/send_message/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_wrong_type(self):
        body1 = {
            'chat_tag': '@group_5',
            'user_id': 5,
            'type': 'image',
            'content': 'Hello',
        }
        body2 = {
            'chat_tag': '@group_5',
            'user_id': 5,
            'type': 'qwerty',
            'content': 'Hello',
        }
        response1 = self.Client.post('/chats/send_message/', json.dumps(body1), content_type="application/json")
        response2 = self.Client.post('/chats/send_message/', json.dumps(body2), content_type="application/json")
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response2.status_code, 400)

    def test_not_a_member(self):
        body = {
            'chat_tag': '@@Miley@Alex',
            'user_id': 1,
            'type': 'text',
            'content': 'Hello',
        }
        response = self.Client.post('/chats/send_message/', json.dumps(body), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_method_not_allowed(self):
        response = self.Client.get('/chats/send_message/')
        self.assertEqual(response.status_code, 405)


class GetChatListTest(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.Client = Client()

    def test_correct(self):
        response1 = self.Client.get('/chats/chat_list/?id=2')
        response2 = self.Client.get('/chats/chat_list/?id=5')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_no_user(self):
        response1 = self.Client.get('/chats/chat_list/?id=500')
        response2 = self.Client.get('/chats/chat_list/')
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response2.status_code, 400)

    def test_method_not_allowed(self):
        response = self.Client.post('/chats/chat_list/?id=2')
        self.assertEqual(response.status_code, 405)


class GetMessagesListTest(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.Client = Client()

    def test_correct(self):
        chat = Chat.objects.get(tag='@group_4')
        user = User.objects.get(id=5)
        Message.objects.create(chat=chat,
                               user=user,
                               type='image',
                               url='blob')

        response = self.Client.get('/chats/chat/?tag=@group_4')
        self.assertEqual(response.status_code, 200)

    def test_no_chat(self):
        response = self.Client.get('/chats/chat/?tag=@gbgffgvf')
        self.assertEqual(response.status_code, 400)

    def test_method_not_allowed(self):
        response = self.Client.post('/chats/chat/?tag=@group_4')
        self.assertEqual(response.status_code, 405)


class ChatDetailTest(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.Client = Client()

    def test_correct(self):
        response = self.Client.get('/chats/chat_detail/')
        self.assertEqual(response.status_code, 200)

    def test_method_not_allowed(self):
        response = self.Client.post('/chats/chat_detail/')
        self.assertEqual(response.status_code, 405)


class MockTest(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        self.Client = Client()

    @patch('chats.views.get_message_info')
    def test_chat_info(self, get_message_info_mock):
        self.Client.get('/chats/chat/?tag=@group_4')
        self.Client.get('/chats/chat/?tag=@gbgffgvf')
        self.Client.get('/chats/chat_list/?id=2')

        self.assertEqual(get_message_info_mock.call_count, 50)
