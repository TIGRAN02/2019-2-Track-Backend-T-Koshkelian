from django.urls import path

from users.views import *

urlpatterns = [
    path('create_user/', create_user, name='create_user'),
    path('auth/', authenticate, name='auth'),
    path('logout/', logout_view, name='logout'),
    path('change_password/', change_password, name='change_password'),
    path('find_users/', find_users, name='find_users'),
    path('profile/', user_profile, name='chat_profile'),
    path('set_user/', set_user, name='set_user'),
    path('read_message/', read_message, name='read_message'),
    path('check_auth/', check_auth, name='check_auth'),
]
