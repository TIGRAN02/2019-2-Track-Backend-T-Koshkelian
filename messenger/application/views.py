from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.core.cache import cache
import jwt

from django.conf import settings
from chats.models import *
from users.models import *

people = [
    'Tigran',
    'Martin',
    'Jennifer Ashley',
    'Anton Ivanov',
    'Michael',
    'Sergey',
    'Miley',
    'Sam',
    'Alex',
    'Millie Bobby Brown',
]


def fill_db(request):
    for i in range(len(people)):
        User.objects.create(nick=people[i],
                            username='@' + people[i].replace(" ", ""),
                            tag='@' + people[i].replace(" ", ""),
                            password='@' + people[i].replace(" ", ""))
    for i in range(len(people) - 2):
        first = User.objects.get(tag='@' + people[i].replace(" ", ""))
        second = User.objects.get(tag='@' + people[i + 1].replace(" ", ""))
        third = User.objects.get(tag='@' + people[i + 2].replace(" ", ""))

        Chat.objects.create(name=first.nick + ' with ' + second.nick,
                            tag='@' + first.tag + second.tag,
                            author=first)
        Chat.objects.create(name=first.nick + ' with ' + third.nick,
                            tag='@' + first.tag + third.tag,
                            author=first)

        chat12 = Chat.objects.get(tag='@' + first.tag + second.tag)
        chat13 = Chat.objects.get(tag='@' + first.tag + third.tag)

        Member.objects.create(user=first, chat=chat12)
        Member.objects.create(user=first, chat=chat13)
        Member.objects.create(user=second, chat=chat12)
        Member.objects.create(user=third, chat=chat13)

        for j in range(10):
            Message.objects.create(chat=chat12, user=first, content='Message ' + str(j + 1) + ' from ' + first.nick)
            Message.objects.create(chat=chat13, user=first, content='Message ' + str(j + 1) + ' from ' + first.nick)
            Message.objects.create(chat=chat12, user=second,
                                   content='Message ' + str(j + 1) + ' from ' + second.nick)
            Message.objects.create(chat=chat13, user=third, content='Message ' + str(j + 1) + ' from ' + third.nick)

    for i in range(len(people) - 5):
        author = User.objects.get(tag='@' + people[i].replace(" ", ""))

        Chat.objects.create(name='Channel by ' + author.nick,
                            tag='@' + author.tag + 'Channel',
                            is_channel=True,
                            author=author)

        chat = Chat.objects.get(tag='@' + author.tag + 'Channel')

        for j in range(5):
            curr_user = User.objects.get(tag='@' + people[i + j].replace(" ", ""))
            Member.objects.create(user=curr_user, chat=chat)

        for j in range(20):
            Message.objects.create(chat=chat, user=author,
                                   content='Message ' + str(j + 1) + ' from author ' + author.nick)

    for i in range(len(people) - 5):
        Chat.objects.create(name='Group started by ' + people[i],
                            tag='@group_' + str(i + 1),
                            is_group=True,
                            author=User.objects.get(tag='@' + people[i].replace(" ", "")))

        chat = Chat.objects.get(tag='@group_' + str(i + 1))

        for j in range(5):
            this_user = User.objects.get(tag='@' + people[i + j].replace(" ", ""))
            Member.objects.create(user=this_user, chat=chat)

            for k in range(10):
                Message.objects.create(chat=chat,
                                       user=this_user,
                                       content='Message ' + str(k + 1) + ' from member ' + this_user.nick)

    return HttpResponse('Database filled')


def logout_all(request):
    User.objects.all().update(is_authorised=False)
    return HttpResponse('Logout successful')


def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})


def centrifugo_token(request):
    token = jwt.encode({'sub': str(request.user.id)}, settings.CENTRIFUGE_SECRET, algorithm="HS256").decode()
    return JsonResponse({'token': token})


if __name__ == '__main__':
    cache.clear()
