from django.urls import path
from chats.views import *


urlpatterns = [
    path('index/', index, name='index'),
    path('create_chat/', create_chat, name='create_chat'),
    path('send_message/', send_message, name='send_message'),
    path('chat_list/', chat_list, name='chat_list'),
    path('chat/<str:chat_tag>/', one_chat, name='one_chat'),
]
