from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from apps.character.models import Character

class CharacterSelectionForm(forms.Form):
    characters = forms.ModelMultipleChoiceField(
        queryset=Character.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )