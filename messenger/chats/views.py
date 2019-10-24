from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        return HttpResponseNotAllowed(['GET'])


@csrf_exempt
def chat_list(request):
    if request.method == 'GET':
        return JsonResponse({'chats': ['Общество целых бокалов',
                                       'Дженнифер Эшли',
                                       'Антон Иванов',
                                       'Серёга (должен 2000)',
                                       'Общество разбитых бокалов',
                                       'Сэм с Нижнего',
                                       'Айрат работа',
                                       'Кеша армия',
                                       'Первый курс ФПМИ-Наука 2019-2020']})
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
