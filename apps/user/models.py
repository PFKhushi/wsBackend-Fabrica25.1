from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.text import slugify
from apps.character import models as char
from django.contrib.auth.models import User


# Create your models here.

class ListChars(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    characters = models.ManyToManyField(char.Character, related_name="users", blank=True, null=True)

    def __str__(self):
        return f"{ self.user.username }{ self.characters.name }"
    