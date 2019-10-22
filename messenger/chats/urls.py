from django.urls import path
from chats.views import *


urlpatterns = [
    path('index/', index, name='index'),
    path('profile/', chat_profile, name='chat_profile'),
    path('chatList/', chat_list, name='chat_list'),
    path('chat/', one_chat, name='one_chat'),
    path('contacts/', contacts, name='contacts')
]
