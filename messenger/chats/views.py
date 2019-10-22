from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        return HttpResponse(status=405)


def chat_profile(request):
    if request.method == 'GET':
        age = request.GET.get('age')
        if age is None:
            age = 17
        name = request.GET.get('name')
        if name is None:
            name = 'Tigran'
        num_of_messages = request.GET.get('num_of_messages')
        if num_of_messages is None:
            num_of_messages = 10
        return JsonResponse({'name': name, 'age': age, 'messages': num_of_messages})
    else:
        return HttpResponse(status=405)


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
        return HttpResponse(status=405)


def one_chat(request):
    if request.method == 'GET':
        chat_name = request.GET.get('name')
        if chat_name is None:
            raise Http404('A chat name is needed (provide in \'name\' parameter)')
        return JsonResponse({chat_name: [chat_name + ' Message 1',
                                         chat_name + ' Message 2',
                                         chat_name + ' Message 3',
                                         chat_name + ' Message 4',
                                         chat_name + ' Message 5',
                                         chat_name + ' Message 6',
                                         chat_name + ' Message 7',
                                         '...',
                                         chat_name + ' Message 239']})
    else:
        return HttpResponse(status=405)


def contacts(request):
    if request.method == 'GET':
        return JsonResponse({'contacts': ['Общество целых бокалов',
                                          'Дженнифер Эшли',
                                          'Антон Иванов',
                                          'Серёга (должен 2000)',
                                          'Общество разбитых бокалов',
                                          'Сэм с Нижнего',
                                          'Айрат работа',
                                          'Кеша армия',
                                          'Первый курс ФПМИ-Наука 2019-2020',
                                          'Контакт без сообщений',
                                          'Контакт в чс',
                                          'Игнорить этот контакт']})
    else:
        return HttpResponse(status=405)
