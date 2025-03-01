import os
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RickNMortyDjango.settings')

# Configure Django
django.setup()

from django.utils import timezone


utc = timezone.now()
now = timezone.localtime()
print(utc)
print(now)