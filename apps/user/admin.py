from django.contrib import admin
from .models import ListChars

# Register your models here.

class ListAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('user', 'characters')
    
admin.site.register(ListChars, ListAdmin)  