from django.contrib import admin
from .models import *

# Register your models here.
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'species', 'subspecies', 'gender', 'origin', 'location', 'created')
    list_filter = ('id', 'name', 'status', 'species', 'subspecies', 'gender', 'origin', 'location', 'created')
    prepopulated_fields = {'slug': ('name', 'id',)}

class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'air_date', 'episode_code', 'created')
    list_filter = ('id', 'name', 'air_date', 'episode_code', 'created')
    prepopulated_fields = {'slug': ('name', 'id',)}

class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location_type', 'dimension', 'created')
    list_filter = ('id', 'name', 'location_type', 'dimension', 'created')
    prepopulated_fields = {'slug': ('id', 'name',)}
    
admin.site.register(Episode, EpisodeAdmin)  
admin.site.register(Location, LocationAdmin)
admin.site.register(Character, CharacterAdmin)