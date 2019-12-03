import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from users.forms import *


@csrf_exempt
@require_GET
def find_users(request):
    try:
        users = list(User.objects.filter(username__startswith=request.GET.get('name')).values('id', 'username'))
    except ValueError:
        users = list(User.objects.filter(tag__startswith=request.GET.get('tag')).values('id', 'username', 'tag'))
    return JsonResponse({
        'users': users
    })


@csrf_exempt
@require_GET
def user_profile(request):
    try:
        if request.GET.get('id') is not None:
            curr_user = User.objects.get(id=request.GET.get('id'))
        else:
            curr_user = User.objects.get(tag=request.GET.get('tag'))
    except User.DoesNotExist:
        return JsonResponse({'error': 'no such user'}, status=400)
    return JsonResponse({'name': curr_user.username,
                         'tag': curr_user.tag,
                         'bio': curr_user.bio,
                         'id': curr_user.id})


@csrf_exempt
@require_POST
def set_user(request):
    form = SetUserForm(json.loads(request.body))
    if form.is_valid():
        form.save()
        return JsonResponse({
            'msg': 'Данные пользователя изменены',
        })
    else:
        return JsonResponse({'errors': form.errors}, status=400)


@csrf_exempt
@require_GET
def contacts(request):
    users = list(User.objects.all().values('username'))
    return JsonResponse({'contacts': users})


@csrf_exempt
@require_POST
def read_message(request):
    form = ReadMessageForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'msg': 'Сообщение помечено как прочитанное',
        })
    else:
        return JsonResponse({'errors': form.errors}, status=400)

