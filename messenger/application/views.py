from django.http import HttpResponse
from chats.models import *
from users.models import *

people = [
  'Мартин',
  'Дженнифер Эшли',
  'Антон Иванов',
  'Михаил',
  'Серёга',
  'Серый',
  'Сэм',
  'Алекс',
  'Милли Бобби Браун',
  'Тигран',
]


def fill_db(request):
    for i in range(len(people)):
        User.objects.create(username=people[i], tag='@' + people[i], nick=people[i])
    for i in range(len(people) - 2):
        first = User.objects.get(tag='@' + people[i])
        second = User.objects.get(tag='@' + people[i + 1])
        third = User.objects.get(tag='@' + people[i + 2])

        Chat.objects.create(name=first.tag + ' with ' + second.tag,
                            tag='@' + first.tag + second.tag,
                            author=first)
        Chat.objects.create(name=first.tag + ' with ' + third.tag,
                            tag='@' + first.tag + third.tag,
                            author=first)

        chat12 = Chat.objects.get(tag='@' + first.tag + second.tag)
        chat13 = Chat.objects.get(tag='@' + first.tag + third.tag)

        Member.objects.create(user=first, chat=chat12)
        Member.objects.create(user=first, chat=chat13)
        Member.objects.create(user=second, chat=chat12)
        Member.objects.create(user=third, chat=chat13)

        for j in range(10):
            Message.objects.create(chat=chat12, user=first, content='Message #' + str(j) + ' from ' + first.tag)
            Message.objects.create(chat=chat13, user=first, content='Message #' + str(j) + ' from ' + first.tag)
            Message.objects.create(chat=chat12, user=second, content='Message #' + str(j) + ' from ' + second.tag)
            Message.objects.create(chat=chat13, user=third, content='Message #' + str(j) + ' from ' + third.tag)

    for i in range(len(people) - 5):
        author = User.objects.get(tag='@' + people[i])

        Chat.objects.create(name='Channel by ' + author.tag,
                            tag='@' + author.tag + 'Channel',
                            is_channel=True,
                            author=author)

        chat = Chat.objects.get(tag='@' + author.tag + 'Channel')

        for j in range(5):
            curr_user = User.objects.get(tag='@' + people[i + j])
            Member.objects.create(user=curr_user, chat=chat)

        for j in range(20):
            Message.objects.create(chat=chat, user=author, content='Message #' + str(j) + ' from author ' + author.tag)

    for i in range(len(people) - 5):
        Chat.objects.create(name='Group started by @' + people[i],
                            tag='@group#' + str(i),
                            is_group=True,
                            author=User.objects.get(tag='@' + people[i]))

        chat = Chat.objects.get(tag='@group#' + str(i))

        for j in range(5):
            this_user = User.objects.get(tag='@' + people[i + j])
            Member.objects.create(user=this_user, chat=chat)

            for k in range(10):
                Message.objects.create(chat=chat,
                                       user=this_user,
                                       content='Message #' + str(j) + ' from member ' + this_user.tag)

    return HttpResponse('Database filled')
