from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chats import views

router = DefaultRouter()
router.register(r'general', views.UserViewSet, basename='UserViewSet')

urlpatterns = [
    path('', include(router.urls)),
    path('create_chat/', views.create_chat, name='create_chat'),
    path('send_message/', views.send_message, name='send_message'),
    path('chat_list/', views.chat_list, name='chat_list'),
    path('chat_detail/', views.chat_detail, name='chat_detail'),
    path('chat/', views.one_chat, name='one_chat')
]
