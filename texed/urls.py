from django.urls import path
from . import views

urlpatterns = [
    path('users', views.getUsers, name='getUsers'),
    path('start/<int:pk>', views.startChat, name='startChat'),
    path('getchat/<int:pk>', views.getChat, name='getChat'),
    path('getchats', views.getChats, name='getChats'),
    path('api/<int:pk>', views.messageApi, name='api'),
    path('api/chat', views.chatApi, name='api-chat'),
    path('search', views.test, name='search')
]