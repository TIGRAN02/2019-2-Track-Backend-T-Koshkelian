import json

from django.db.models import F
from django.http import JsonResponse, HttpResponse
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt  # , csrf_protect
from django.views.decorators.http import require_POST, require_GET
from rest_framework import viewsets
from rest_framework.decorators import action

from chats.forms import *
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @staticmethod
    # @method_decorator(cache_page(60 * 15))
    @action(methods=['get'], detail=False)
    def members(request, *args, **kwargs):
        result = []
        members = Member.objects.filter(chat__id=request.GET.get('chat_id')). \
            values_list('user__id', flat=True).order_by('id')
        for i in list(members):
            result.append(User.objects.get(id=i))
        serializer = UserSerializer(result, many=True)
        return JsonResponse(serializer.data, safe=False)


# @cache_page(60 * 15)
@csrf_exempt
@require_POST
def create_chat(request):
    form = NewChatForm(json.loads(request.body))
    if form.is_valid():
        form.save()

        return JsonResponse({
            'msg': 'Чат создан',
        })
    else:
        return JsonResponse({'errors': form.errors}, status=400)


# @cache_page(60 * 15)
@csrf_exempt
@require_POST
def send_message(request):
    form = SendMessageForm(json.loads(request.body))
    if form.is_valid():
        form.save()
        return JsonResponse({
            'msg': 'Сообщение отправлено'
        })
    else:
        return JsonResponse({'errors': form.errors}, status=400)


# @cache_page(60 * 15)
@csrf_exempt
@require_GET
def chat_list(request):
    try:
        User.objects.get(id=request.GET.get('id'))
    except User.DoesNotExist:
        return JsonResponse({'errors': 'no such user'}, status=400)
    chats = list(Chat.objects.all().values('name', 'tag'))
    count = len(chats)
    iterator = 0
    while iterator < count:
        try:
            Member.objects.get(chat=Chat.objects.get(tag=chats[iterator]['tag']),
                               user=User.objects.get(id=request.GET.get('id')))
        except Member.DoesNotExist:
            chats.pop(iterator)
            count -= 1
            continue
        curr_messages = Message.objects.filter(chat__tag=chats[iterator]['tag'])
        chats[iterator]['indicator'] = len(curr_messages)
        if len(curr_messages) > 0:
            last_mess = curr_messages[0]
            chats[iterator]['lastType'] = last_mess.type
            chats[iterator]['lastMessage'] = last_mess.content or last_mess.url
            chats[iterator]['lastTime'] = last_mess.time.strftime('%H:%M')
        else:
            chats[iterator]['lastType'] = ''
            chats[iterator]['lastMessage'] = ''
            chats[iterator]['lastTime'] = ''
        iterator += 1
    return JsonResponse({'chats': chats})


# @cache_page(60 * 15)
@csrf_exempt
@require_GET
def one_chat(request):
    try:
        chat = Chat.objects.get(tag=request.GET.get('tag'))
    except Chat.DoesNotExist:
        return HttpResponse('Chat does not exist', status=400)
    messages = Message.objects.annotate(whose=F('user__id')).filter(chat=chat).values('id',
                                                                                      'content',
                                                                                      'time',
                                                                                      'type',
                                                                                      'whose')
    for i in range(len(messages)):
        get_message_info()
        messages[i]['time'] = messages[i]['time'].strftime('%H:%M')
        if messages[i]['type'] != 'text':
            messages[i]['url'] = Message.objects.get(id=messages[i]['id']).url
    return JsonResponse({'messages': list(messages)})


# @cache_page(60 * 15)
@csrf_exempt
@require_GET
def chat_detail(request):
    chat = Chat.objects.annotate(whose=F('author__id'), channel=F('is_channel')). \
        filter(tag=request.GET.get('tag')). \
        values('whose', 'channel')
    return JsonResponse({'chat': list(chat)})


def get_message_info():
    return 0
