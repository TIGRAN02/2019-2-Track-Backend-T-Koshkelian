from __future__ import absolute_import, unicode_literals

from celery import shared_task
from users.models import User


@shared_task
def count_auth_users():
    print(User.objects.filter(is_authorised=True).count())
