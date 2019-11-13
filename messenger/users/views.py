from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import *


@csrf_exempt
def find_users(request):
    if request.method == 'GET':
        user = User.objects.filter(name__in=request.GET.get('name'))
        return HttpResponse
    else:
        return HttpResponseNotAllowed(['GET'])


@csrf_exempt
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
        return HttpResponseNotAllowed(['GET'])


@csrf_exempt
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
        return HttpResponseNotAllowed(['GET'])
