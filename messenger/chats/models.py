from django.db import models
from django.utils.timezone import now


class Chat(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    tag = models.CharField(max_length=50, unique=True, verbose_name='Тег для поиска')
    is_group = models.BooleanField(default=False, verbose_name='Является ли чат группой')
    is_channel = models.BooleanField(default=False, verbose_name='Является ли чат каналом')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Автор чата')
    bio = models.TextField(blank=True, null=True, verbose_name='Описание чата')
    last_message = models.TextField(blank=True, null=True, verbose_name='Последнее сообщение в чате')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name='Чат')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    content = models.TextField(null=True, verbose_name='Содержание')
    time = models.DateTimeField(default=now, null=True, verbose_name='Время отправки')
    type = models.CharField(max_length=15, default='text', verbose_name='Тип сообщения')
    url = models.URLField(null=True, verbose_name='Ссылка на фото')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-time']
