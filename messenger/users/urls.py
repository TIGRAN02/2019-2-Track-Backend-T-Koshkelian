from django.urls import path
from users.views import *


path('profile/', chat_profile, name='chat_profile'),
path('contacts/', contacts, name='contacts')
