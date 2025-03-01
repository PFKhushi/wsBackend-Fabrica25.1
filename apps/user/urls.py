from .views import *
from django.urls import path, include



urlpatterns = [
    path('login/', user_login, name='login'),
]
