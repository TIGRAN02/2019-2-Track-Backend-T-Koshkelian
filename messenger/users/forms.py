from django import forms
from chats.models import Chat, Message
from users.models import User, Member


class ReadMessageForm(forms.Form):
    chat_id = forms.IntegerField()
    user_id = forms.IntegerField()
    message_id = forms.IntegerField()

    def clean_chat_id(self):
        try:
            Chat.objects.get(id=self.cleaned_data['chat_id'])
        except Chat.DoesNotExist:
            self.add_error('chat_id', 'no such chat')
        return self.cleaned_data['chat_id']

    def clean_user_id(self):
        try:
            User.objects.get(id=self.cleaned_data['user_id'])
        except User.DoesNotExist:
            self.add_error('user_id', 'no such user')
        return self.cleaned_data['user_id']

    def clean_message_id(self):
        try:
            Message.objects.get(id=self.cleaned_data['message_id'])
        except Message.DoesNotExist:
            self.add_error('message_id', 'no such message')
        return self.cleaned_data['message_id']

    def clean(self):
        chat = Chat.objects.get(id=self.cleaned_data['chat_id'])
        user = User.objects.get(id=self.cleaned_data['user_id'])
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
    bio = forms.CharField(widget=forms.Textarea)
    old_tag = forms.CharField(max_length=50)

    def clean_tag(self):
        if self.cleaned_data['tag'][0] != '@':
            self.add_error('tag', 'not a valid tag')
        return self.cleaned_data['tag']

    def clean_old_tag(self):
        try:
            User.objects.get(tag=self.cleaned_data['old_tag'])
        except User.DoesNotExist:
            self.add_error('old_tag', 'no such user')
        return self.cleaned_data['old_tag']

    def clean(self):
        if self.cleaned_data['tag'] != self.cleaned_data['old_tag']:
            try:
                User.objects.get(tag=self.cleaned_data['tag'])
                self.add_error('tag', 'tag already exists')
            except User.DoesNotExist:
                pass

    def save(self):
        User.objects.filter(tag=self.cleaned_data['old_tag']).update(username=self.cleaned_data['name'],
                                                                     tag=self.cleaned_data['tag'],
                                                                     bio=self.cleaned_data['bio'])
