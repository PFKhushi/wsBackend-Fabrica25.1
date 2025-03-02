from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from apps.character import models as model
from datetime import datetime
from apps.user.models import ListChars
from django.contrib.auth.models import User

BASE_URL = "https://rickandmortyapi.com/api/"
# Create your views here.

def index(request):
    
    return render(request, "core/index.html")



def search_character(request):
    
    try:
        full_url = f"{BASE_URL}character/?name={request.GET.get('character')}"
        requisition = requests.get(full_url)
        
        response = requisition.json()

        characters = []
        for char in response['results']:
            character, created = model.Character.objects.update_or_create(
                id=char['id'],  # Unique identifier
                defaults={  # Fields to update if the character exists
                    'name': char['name'],
                    'status': model.Status(char['status'][0]),
                    'species': char['species'],
                    'subspecies': char['type'],
                    'gender': model.Gender(char['gender'][0]),
                    'origin': get_location(char['origin']['url']),
                    'location': get_location(char['location']['url']),
                    'image_url': char['image'],
                    'url': char['url'],
                    'created': char['created'],
                    }
                )
            episodes = char['episode']
            character.episode.set(get_episodes(episodes))
            
            characters.append(character)
        return render(request, "core/character.html", {"characters": characters})
    except ValueError as e:
        return render(request, "core/error.html", {'e': e})

def get_location(url):
    
    response = requests.get(url).json()
    
    location, created = model.Location.objects.update_or_create(
                id=response['id'],
                defaults={
                    'name': response['name'],
                    'location_type': response['type'],
                    'dimension': response['dimension'],
                    'url': response['url'],
                    'created': response['created'],
                }
            )
    return location

def get_episode(url):
    response = requests.get(url).json()
    
    episode, created = model.Episode.objects.update_or_create(
        id = response['id'],
        defaults={
        'id': response['id'],
        'name': response['name'],
        'air_date': datetime.strptime(response['air_date'], "%B %d, %Y").date(),
        'episode_code': response['episode'],
        'url': response['url'],
        'created': response['created'],
        }
    )
    return episode
    
def get_episodes(urls):
    
    temp = []
    
    for url in urls:
        temp.append(get_episode(url))
    return temp

#def save_character(request):
#    if request.user.is_authenticated:
#        id = 1 #request.GET.get('character.id')
#        character = model.Character.objects.get(id=id)  # Get the character instance
#        
#        # Ensure the user has a ListChars entry or create one
#        user_list, created = ListChars.objects.update_or_create(
#            user=request.user,  # Set the user field
#            defaults={'characters': character}  # Set or update character
#        )
#
#        return redirect('index')  # Redirect after saving
#
#    return redirect('login')  # Redirect to login if not authenticated