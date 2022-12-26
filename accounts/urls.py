from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.loginpage, name='loginpage'),
    path('home', views.home, name='home'),
    path('logout', views.logoutpage, name='logout')
]