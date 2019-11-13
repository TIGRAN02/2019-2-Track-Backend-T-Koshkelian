from django.urls import path
from users.views import *


urlpatterns = [
    path('profile/', chat_profile, name='chat_profile'),
    path('contacts/', contacts, name='contacts'),
    path('find_users/', find_users, name='find_users')
]

