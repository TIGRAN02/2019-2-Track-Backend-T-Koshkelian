from django.urls import path
from users.views import *


urlpatterns = [
    path('find_users/', find_users, name='find_users'),
    path('profile/', chat_profile, name='chat_profile'),
    path('contacts/', contacts, name='contacts'),
    path('read_message/', read_message, name='read_message'),
]

