from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(theme, text, email):
    send_mail(
        theme,
        text,
        'koshkelian.ta@phystech.edu',
        [email],
        fail_silently=False
    )
