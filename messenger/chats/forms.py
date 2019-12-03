from django import forms
from chats.models import *
from users.models import *


class NewChatForm(forms.Form):
    first_tag = forms.CharField(max_length=50)
    second_tag = forms.CharField(max_length=50)

    def clean_first_tag(self):
        first = self.cleaned_data['first_tag']
        try:
            User.objects.get(tag=first)
        except User.DoesNotExist:
            self.add_error('first_tag', 'no such user')
        return first

    def clean_second_tag(self):
        second = self.cleaned_data['second_tag']
        try:
            User.objects.get(tag=second)
        except User.DoesNotExist:
            self.add_error('second_tag', 'no such user')
        return second

    def clean(self):
        first = self.cleaned_data['first_tag']
        second = self.cleaned_data['second_tag']
        try:
            Chat.objects.get(tag='@' + first + second)
            self.add_error('chat', 'already exists')
        except Chat.DoesNotExist:
            try:
                Chat.objects.get(tag='@' + second + first)
                self.add_error('chat', 'already exists')
            except Chat.DoesNotExist:
                pass

    def save(self):
        first = self.cleaned_data['first_tag']
        second = self.cleaned_data['second_tag']

        first_user = User.objects.get(tag=first)
        second_user = User.objects.get(tag=second)

        Chat.objects.create(name=first + ' with ' + second, tag='@' + first + second)
        new_chat = Chat.objects.get(tag='@' + first + second)

        Member.objects.create(user=first_user, chat=new_chat)
        Member.objects.create(user=second_user, chat=new_chat)


class SendMessageForm(forms.Form):
    chat_tag = forms.CharField(max_length=50)
    user_id = forms.CharField(max_length=50)
    type = forms.CharField(max_length=15)
    content = forms.CharField(required=False, max_length=1024)
    url = forms.CharField(required=False, max_length=100)

    def clean_chat_tag(self):
        chat = self.cleaned_data['chat_tag']
        try:
            Chat.objects.get(tag=chat)
        except Chat.DoesNotExist:
            self.add_error('chat_tag', 'no such chat')
        return self.cleaned_data['chat_tag']

    def clean_user_id(self):
        user = self.cleaned_data['user_id']
        try:
            User.objects.get(id=user)
        except User.DoesNotExist:
            self.add_error('user_id', 'no such user')
        return self.cleaned_data['user_id']

    def clean(self):
        if self.cleaned_data['type'] == 'text':
            if self.cleaned_data['content'] is None:
                self.add_error('content', 'text message with no content')
        else:
            if self.cleaned_data['type'] == 'audio' or self.cleaned_data['type'] == 'image':
                if self.cleaned_data['url'] is None:
                    self.add_error('url', self.cleaned_data['type'] + ' message with no url')

        chat = Chat.objects.get(tag=self.cleaned_data['chat_tag'])
        user = User.objects.get(id=self.cleaned_data['user_id'])
        try:
            Member.objects.get(user=user, chat=chat)
        except Member.DoesNotExist:
            self.add_error('user', 'no such user in this chat')

    def save(self):
        chat = Chat.objects.get(tag=self.cleaned_data['chat_tag'])
        user = User.objects.get(id=self.cleaned_data['user_id'])

        if self.cleaned_data['type'] == 'text':
            Message.objects.create(chat=chat,
                                   user=user,
                                   content=self.cleaned_data['content'])
        else:
            Message.objects.create(chat=chat,
                                   user=user,
                                   type=self.cleaned_data['type'],
                                   url=self.cleaned_data['url'])
