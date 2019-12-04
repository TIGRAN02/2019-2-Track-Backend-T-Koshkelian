from django import forms

from chats.models import *
from users.models import *


class NewChatForm(forms.Form):
    name = forms.CharField(max_length=50)
    tag = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    creator = forms.CharField(max_length=50)
    members = forms.CharField(widget=forms.Textarea, required=False)
    is_channel = forms.CharField(max_length=10)
    
    def clean_tag(self):
        try:
            Chat.objects.get(tag=self.cleaned_data['tag'])
            self.add_error('tag', 'tag already exists')
        except Chat.DoesNotExist:
            pass
        
        to_ret = self.cleaned_data['tag'].replace(" ", "")
        if self.cleaned_data['tag'][0] != '@':
            to_ret = '@' + to_ret
        return to_ret
    
    def clean_creator(self):
        try:
            User.objects.get(id=self.cleaned_data['creator'])
        except User.DoesNotExist:
            self.add_error('creator', 'no such user')
        return self.cleaned_data['creator']
    
    def clean_members(self):
        real_members = self.cleaned_data['members'].split(' ')
    
        for i in range(len(real_members)):
            try:
                User.objects.get(tag=real_members[i])
            except User.DoesNotExist:
                self.add_error('members', 'no user')
    
        return self.cleaned_data['members']
    
    def clean(self):
        real_members = self.cleaned_data['members'].split(' ')
        
        if len(real_members) == 0 and not self.cleaned_data['is_channel']:
            self.add_error('members', 'chat must have members')

    def save(self):
        real_members = self.cleaned_data['members'].split(' ')
    
        if len(real_members) > 1:
            is_group = True
        else:
            is_group = False
        
        Chat.objects.create(name=self.cleaned_data['name'],
                            tag=self.cleaned_data['tag'],
                            bio=self.cleaned_data['bio'],
                            author=User.objects.get(id=self.cleaned_data['creator']),
                            is_channel=self.cleaned_data['is_channel'],
                            is_group=is_group)

        chat = Chat.objects.get(tag=self.cleaned_data['tag'])
        
        Member.objects.create(chat=chat,
                              user=User.objects.get(id=self.cleaned_data['creator']))

        for i in range(len(real_members)):
            curr_user = User.objects.get(tag=real_members[i])
            Member.objects.create(user=curr_user, chat=chat)


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
