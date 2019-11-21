from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from chats.forms import *


@csrf_exempt
@require_GET
def index(request):
    return render(request, 'index.html')


@csrf_exempt
@require_POST
def create_chat(request):
    form = NewChatForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'msg': 'Чат создан',
        })
    else:
        return JsonResponse({'errors': form.errors}, status=400)


@csrf_exempt
@require_POST
def send_message(request):
    form = SendMessageForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'msg': 'Сообщение отправлено'
        })
    else:
        return JsonResponse({'errors': form.errors}, status=400)


@csrf_exempt
@require_GET
def chat_list(request):
    chats = Chat.objects.all().values('name')
    return JsonResponse({'chats': list(chats)})


@csrf_exempt
@require_GET
def one_chat(request, chat_tag):
    try:
        chat = Chat.objects.get(tag=chat_tag)
    except Chat.DoesNotExist:
        return HttpResponse('No such chat')
    messages = Message.objects.filter(chat=chat).values('content')
    return JsonResponse({'Messages': list(messages)})
