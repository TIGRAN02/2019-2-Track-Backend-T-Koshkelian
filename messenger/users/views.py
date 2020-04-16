import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from chats.tasks import send_email
from users.forms import *


@csrf_exempt
@require_POST
def create_user(request):
    form = CreateUserForm(json.loads(request.body))
    if form.is_valid():
        form.save()

        if json.loads(request.body)['tag'][0] != '@':
            tag = '@' + json.loads(request.body)['tag'].replace(" ", "")
        else:
            tag = json.loads(request.body)['tag'].replace(" ", "")

        return JsonResponse({
            'msg': 'Пользователь успешно создан',
            'id': list(User.objects.filter(tag=tag).values('id'))
        })
    else:
        return JsonResponse({'errors': form.errors}, status=400)


@csrf_exempt
@require_POST
def authenticate(request):
    data = json.loads(request.body)
    form = AuthForm(data)
    if form.is_valid():
        form.save()
        user = User.objects.get(tag=data['tag'])
        return JsonResponse({'id': user.id})
    else:
        return JsonResponse({'errors': form.errors}, status=400)


@csrf_exempt
@require_GET
def logout_view(request):
    try:
        User.objects.filter(id=request.GET.get('id')).update(is_authorised=False)
        return JsonResponse({'msg': 'logout successful'})
    except User.DoesNotExist:
        return JsonResponse({'errors': 'no such user'}, status=400)


@csrf_exempt
@require_GET
def check_auth(request):
    user_id = request.GET.get('id')
    try:
        user = User.objects.get(id=user_id)
        if user.is_authorised:
            return JsonResponse({'auth': True})
        else:
            return JsonResponse({'auth': False})
    except User.DoesNotExist:
        return JsonResponse({'errors': 'no such user'}, status=400)


@csrf_exempt
@require_POST
def change_password(request):
    form = ChangePasswordForm(json.loads(request.body))
    if form.is_valid():
        form.save()
        return JsonResponse({
            'msg': 'Пароль успешно изменен',
        })
    else:
        return JsonResponse({'errors': form.errors}, status=400)


@csrf_exempt
@require_GET
def find_users(request):
    try:
        users = list(User.objects.filter(nick__startswith=request.GET.get('name')).values('id', 'nick'))
    except ValueError:
        users = list(User.objects.filter(tag__startswith=request.GET.get('tag')).values('id', 'nick', 'tag'))
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
            if request.GET.get('tag') is not None:
                curr_user = User.objects.get(tag=request.GET.get('tag'))
            else:
                return JsonResponse({'errors': 'no id or tag'}, status=400)
    except User.DoesNotExist:
        return JsonResponse({'errors': 'no such user'}, status=400)
    return JsonResponse({'name': curr_user.nick,
                         'tag': curr_user.tag,
                         'bio': curr_user.bio, })


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
@require_POST
def read_message(request):
    form = ReadMessageForm(json.loads(request.body))
    if form.is_valid():
        form.save()
        return JsonResponse({
            'msg': 'Сообщение помечено как прочитанное',
        })
    else:
        return JsonResponse({'errors': form.errors}, status=400)

