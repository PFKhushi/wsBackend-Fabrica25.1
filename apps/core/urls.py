from django.urls import path
from apps.core import views
from apps.character.models import Character

urlpatterns = [
    path('', views.index, name="index"),
    path("search/", views.search_character, name="search"),
    #path('save/', views.save_character, name="save_character")
    
]
