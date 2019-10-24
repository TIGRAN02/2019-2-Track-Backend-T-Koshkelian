from django.urls import path
from chats.views import *


urlpatterns = [
    path('index/', index, name='index'),
    path('chat_list/', chat_list, name='chat_list'),
    path('chat/<int:chat_id>/', one_chat, name='one_chat'),
]
