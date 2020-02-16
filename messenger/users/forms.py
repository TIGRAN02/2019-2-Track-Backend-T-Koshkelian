from django import forms

from chats.models import *
from users.models import *


class CreateUserForm(forms.Form):
    name = forms.CharField(max_length=50)
    tag = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    password = forms.CharField(max_length=50)
    
    def clean_tag(self):
        try:
            User.objects.get(tag=self.cleaned_data['tag'])
            self.add_error('tag', 'tag already exists')
            return
        except User.DoesNotExist:
            pass
        if self.cleaned_data['tag'][0] != '@':
            return '@' + self.cleaned_data['tag'].replace(" ", "")
        else:
            return self.cleaned_data['tag'].replace(" ", "")
    
    def save(self):
        if self.cleaned_data['bio'] == '':
            User.objects.create(nick=self.cleaned_data['name'],
                                username=self.cleaned_data['tag'],
                                tag=self.cleaned_data['tag'],
                                password=self.cleaned_data['password'])
        else:
            User.objects.create(nick=self.cleaned_data['name'],
                                username=self.cleaned_data['tag'],
                                tag=self.cleaned_data['tag'],
                                bio=self.cleaned_data['bio'],
                                password=self.cleaned_data['password'])


class AuthForm(forms.Form):
    tag = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    
    def clean_tag(self):
        try:
            User.objects.get(tag=self.cleaned_data['tag'])
        except User.DoesNotExist:
            self.add_error('tag', 'no such user')
            return
        return self.cleaned_data['tag']
    
    def clean(self):
        if self.cleaned_data['tag'] is None:
            return
        correct_pass = User.objects.get(tag=self.cleaned_data['tag']).password
        if self.cleaned_data['password'] != correct_pass:
            self.add_error('password', 'incorrect password')


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=50)
    new_password = forms.CharField(max_length=50)
    tag = forms.CharField(max_length=50)
    
    def clean_tag(self):
        try:
            User.objects.get(tag=self.cleaned_data['tag'])
        except User.DoesNotExist:
            self.add_error('tag', 'no such user')
            return
        return self.cleaned_data['tag']

    def clean(self):
        if self.cleaned_data['tag'] is None:
            return
        if self.cleaned_data['old_password'] != User.objects.get(tag=self.cleaned_data['tag']).password:
            self.add_error('old_password', 'incorrect old password')
    
    def save(self):
        User.objects.filter(tag=self.cleaned_data['tag']).update(password=self.cleaned_data['new_password'])
            

class ReadMessageForm(forms.Form):
    chat_id = forms.IntegerField()
    user_id = forms.IntegerField()
    message_id = forms.IntegerField()

    def clean_chat_id(self):
        try:
            Chat.objects.get(id=self.cleaned_data['chat_id'])
        except Chat.DoesNotExist:
            self.add_error('chat_id', 'no such chat')
            return
        return self.cleaned_data['chat_id']

    def clean_user_id(self):
        try:
            User.objects.get(id=self.cleaned_data['user_id'])
        except User.DoesNotExist:
            self.add_error('user_id', 'no such user')
            return
        return self.cleaned_data['user_id']

    def clean_message_id(self):
        try:
            Message.objects.get(id=self.cleaned_data['message_id'])
        except Message.DoesNotExist:
            self.add_error('message_id', 'no such message')
            return
        return self.cleaned_data['message_id']

    def clean(self):
        if None in [self.cleaned_data['chat_id'], self.cleaned_data['user_id'], self.cleaned_data['message_id']]:
            return
        chat = Chat.objects.get(id=self.cleaned_data['chat_id'])
        user = User.objects.get(id=self.cleaned_data['user_id'])
        message = Message.objects.get(id=self.cleaned_data['message_id'])
        if message.chat != chat:
            self.add_error('message_id', 'no such message in the chat')
        try:
            Member.objects.get(chat=chat, user=user)
        except Member.DoesNotExist:
            self.add_error('user_id', 'no such member')

    def save(self):
        chat = Chat.objects.get(id=self.cleaned_data['chat_id'])
        user = User.objects.get(id=self.cleaned_data['user_id'])
        message = Message.objects.get(id=self.cleaned_data['message_id'])
        curr_member = Member.objects.get(chat=chat, user=user)
        curr_member.last_read_message = message
        curr_member.save()


class SetUserForm(forms.Form):
    name = forms.CharField(max_length=50)
    tag = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    old_tag = forms.CharField(max_length=50)
    old_password = forms.CharField(max_length=50, required=False)
    new_password = forms.CharField(max_length=50, required=False)

    def clean_tag(self):
        if self.cleaned_data['tag'] == '' or self.cleaned_data['tag'][0] != '@':
            self.add_error('tag', 'not a valid tag')
            return
        return self.cleaned_data['tag']

    def clean_old_tag(self):
        try:
            User.objects.get(tag=self.cleaned_data['old_tag'])
        except User.DoesNotExist:
            self.add_error('old_tag', 'no such user')
            return
        return self.cleaned_data['old_tag']

    def clean(self):
        if None in [self.cleaned_data['tag'], self.cleaned_data['old_tag']]:
            return
        if self.cleaned_data['tag'] != self.cleaned_data['old_tag']:
            try:
                User.objects.get(tag=self.cleaned_data['tag'])
                self.add_error('tag', 'tag already exists')
                return
            except User.DoesNotExist:
                pass

        if self.cleaned_data['new_password'] == '':
            return

        if User.objects.get(tag=self.cleaned_data['old_tag']).password != self.cleaned_data['old_password']:
            self.add_error('old_password', 'incorrect password')

    def save(self):
        if self.cleaned_data['new_password'] == '':
            User.objects.filter(tag=self.cleaned_data['old_tag']).update(nick=self.cleaned_data['name'],
                                                                         tag=self.cleaned_data['tag'],
                                                                         bio=self.cleaned_data['bio'])
        else:
            User.objects.filter(tag=self.cleaned_data['old_tag']).update(nick=self.cleaned_data['name'],
                                                                         tag=self.cleaned_data['tag'],
                                                                         bio=self.cleaned_data['bio'],
                                                                         password=self.cleaned_data['new_password'])
