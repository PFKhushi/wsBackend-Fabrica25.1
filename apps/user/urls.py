from . import views
from django.urls import path, include

urlpatterns = [
    path('login_user', views.user_login, name='login'),
    path('logout_user', views.user_logout, name='logout'),
]
