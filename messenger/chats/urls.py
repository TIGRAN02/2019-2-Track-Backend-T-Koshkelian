from django.urls import path

from chats.views import *

urlpatterns = [
    path('create_chat/', create_chat, name='create_chat'),
    path('send_message/', send_message, name='send_message'),
    path('chat_list/', chat_list, name='chat_list'),
    path('chat_detail/', chat_detail, name='chat_detail'),
    path('chat/', one_chat, name='one_chat'),
]
