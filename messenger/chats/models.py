from django.db import models


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
    content = models.TextField(verbose_name='Содержание')
    sent_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время отправки')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-sent_time']


class Attachment(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name='Чат')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    type = models.CharField(max_length=20, verbose_name='Тип')
    url = models.URLField(verbose_name='Ссылка')

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'

