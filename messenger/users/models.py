from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nick = models.CharField(max_length=50, default='Hummingbird', verbose_name='Ник пользователя')
    tag = models.CharField(max_length=50, unique=True, verbose_name='Тег для поиска')
    bio = models.TextField(default='Newborn Hummingbird', blank=True, null=True, verbose_name='Краткое описание')
    avatar = models.ImageField(blank=True, null=True, verbose_name='Фотография')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    chat = models.ForeignKey('chats.Chat', on_delete=models.CASCADE, verbose_name='Чат')
    new_messages = models.IntegerField(blank=True, null=True, verbose_name='Количество новых сообщений')
    last_read_message = models.ForeignKey('chats.Message', on_delete=models.CASCADE, blank=True, null=True,
                                          verbose_name='Последнее прочитанное сообщение')

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
