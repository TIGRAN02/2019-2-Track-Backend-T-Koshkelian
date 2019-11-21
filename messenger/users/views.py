from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from users.forms import *


@csrf_exempt
@require_GET
def find_users(request):
    users = list(User.objects.filter(username__startswith=request.GET.get('name')).values('id', 'username'))
    return JsonResponse({
        'users': users
    })


# TODO: после реализации аутентификации выводить данные нашего пользователя, а не переданного
@csrf_exempt
@require_GET
def chat_profile(request):
    try:
        curr_user = User.objects.get(id=request.GET.get('id'))
    except User.DoesNotExist:
        return HttpResponse('No such user')
    return JsonResponse({'name': curr_user.username,
                         'tag': curr_user.tag,
                         'bio': curr_user.bio})


@csrf_exempt
@require_GET
def contacts(request):
    users = list(User.objects.all().values('username'))
    return JsonResponse({'contacts': users})


@csrf_exempt
@require_POST
def read_message(request):
    form = ReadMessage(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'msg': 'Сообщение помечено как прочитанное',
        })
    else:
        return JsonResponse({'errors': form.errors}, status=400)

