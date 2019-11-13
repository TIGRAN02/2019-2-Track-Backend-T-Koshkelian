from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from chats.models import *
from users.models import *


@csrf_exempt
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        return HttpResponseNotAllowed(['GET'])


@csrf_exempt
def create_chat(request):
    if request.method == 'POST':
        first = str(request.POST.get('first'))
        second = str(request.POST.get('second'))
        first_user = Chat.objects.filter(name=first)
        second_user = Chat.objects.filter(name=second).values('id')
        Chat.objects.create(name=first + ' with ' + second, tag='@' + first + second)
        new_chat = Chat.objects.filter(name=first + ' with ' + second)
        Member.objects.create(user_id=first_user, chat_id=new_chat)
        Member.objects.create(user_id=second_user, chat_id=new_chat)
        return HttpResponse
    else:
        return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def chat_list(request):
    if request.method == 'GET':
        chats = Chat.objects.all().values('name')
        return JsonResponse({'chats': list(chats)})
    else:
        return HttpResponseNotAllowed(['GET'])


@csrf_exempt
def one_chat(request, chat_id):
    if request.method == 'GET':
        return JsonResponse({'Messages': [str(chat_id) + ' Message 1',
                                          str(chat_id) + ' Message 2',
                                          str(chat_id) + ' Message 3',
                                          str(chat_id) + ' Message 4',
                                          str(chat_id) + ' Message 5',
                                          str(chat_id) + ' Message 6',
                                          str(chat_id) + ' Message 7',
                                          '...',
                                          str(chat_id) + ' Message 239']})
    else:
        return HttpResponseNotAllowed(['GET'])
