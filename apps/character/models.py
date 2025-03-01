from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.text import slugify
# Create your models here.

class SlugModel(models.Model):
    slug = models.SlugField(blank=True, null=True, unique=True)

    class Meta:
        abstract = True 

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it's not set
            source_field = getattr(self, "slug_source", "name")
            source_value = getattr(self, source_field)
            base_slug = slugify(source_value)
            slug = base_slug
            counter = 1

            # Ensure slug uniqueness
            while self.__class__.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)

class Gender(models.TextChoices):
    
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    UNKNOWN = 'U', 'Unknown'
    GERNDERLESS = 'G', 'Gernderless'
    
class Status(models.TextChoices):
    DEAD = 'D', 'Dead'
    ALIVE = 'A', 'Alive'
    UNKNOWN = 'U', 'Unknown'

class Location(SlugModel, models.Model):

    id = models.PositiveIntegerField(primary_key=True) # Gets the id from the database
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2), MaxLengthValidator(100)], 
        verbose_name="Nome da localização"
        ) # gets the name of the characte from the database | string
    
    location_type = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2), MaxLengthValidator(100)], 
        verbose_name="Tipo de localização"
        ) # gets the location type from the data base | string 
    
    dimension = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2), MaxLengthValidator(100)], 
        verbose_name="Dimensão da localização"
        ) # gets the location dimension type from the database | string
    
    url = models.URLField(
        verbose_name="URL da Localização", 
        blank=True, 
        null=True
        ) # gets the link to the location's own endpoint. | string
    
    created = models.DateTimeField(verbose_name="Data de criação do localização no banco de dados consumido") # Time at which the location was created in the Rick and morty database. | gets a string
    
    def __str__(self):
        
        return f"Nome: {self.name} Tipo de localização: {self.location_type} Dimensão: {self.dimension}"
    
    
class Character(SlugModel, models.Model):
    
    id = models.PositiveIntegerField(primary_key=True) # Gets the id from the database | string
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2), MaxLengthValidator(100)]
        ) # gets the name of the characte from the database | string

    status = models.CharField(
        verbose_name="Estado do persoganem",
        max_length=1, 
        choices=Status.choices, 
        default = Status.UNKNOWN
        ) # gets the status from the database and converts to Status | string

    species = models.CharField(
        verbose_name="Espécie", 
        max_length=100,
        validators=[MinLengthValidator(2), MaxLengthValidator(100)], 
        blank=True, 
        null=True 
        ) # gets the species name from the database | string 
    
    subspecies = models.CharField(
        max_length=100,
        verbose_name="Subspécie",
        validators=[MinLengthValidator(2), MaxLengthValidator(100)], 
        blank=True, 
        null=True 
        ) # gets the subspecies name from the database | string
    
    gender = models.CharField(
        verbose_name="Genero do personagem",
        max_length=1, 
        choices=Gender.choices, 
        default=Gender.UNKNOWN
        ) # gets a string from the database and assigns a value from Gender | string

    origin = models.ForeignKey(
        Location, 
        verbose_name="Localização de origem do personagem", 
        on_delete=models.SET_NULL, 
        related_name="origin", 
        blank=True, 
        null=True 
        ) # When we create a character it is assigned to one origin location | object

    location = models.ForeignKey(
        "Location", 
        verbose_name="Localização atual do personagem", 
        on_delete=models.SET_NULL, 
        related_name="location", 
        blank=True, 
        null=True 
        ) # a chacter can only be in one location at a time, but a location can have multiple characters | object
    
    image_url = models.URLField(
        verbose_name="URL da imagem",
        blank=True, 
        null=True
        ) # a url link to the image 
    
    episode = models.ManyToManyField(
        "Episode",
        related_name="episode",
        verbose_name="Episodio onde personagem atua", 
        blank=True,
        null=True,
    ) # A character can appear in multiple episodes
    
    url = models.URLField(
        verbose_name="URL do porsonagem", 
        blank=True, 
        null=True
        ) # url to the characters endpoint
    
    created = models.DateTimeField(verbose_name="Data de criação do personagem no banco de dados consumido") # date from the database that says when the character was created
    
    def __str__(self):
        return f"Nome: {self.name} Espécie: {self.species} Subspécie: {self.subspecies} Gênero: {self.gender} Estado: {self.status} Origem: {self.origin} Localização atual: {self.location}"



class Episode(SlugModel, models.Model):
    id = models.PositiveIntegerField(primary_key=True) # gets the id from the database | string
    name = models.CharField(
        max_length=100,
        verbose_name="Nome do episodio",
        validators=[MinLengthValidator(2), MaxLengthValidator(100)]
        ) # gets the name of the characte from the database | string
    
    air_date = models.DateField(verbose_name="Data de estreia do episodio") # gets the date the episode aired | string
    episode_code = models.CharField(
        max_length=100,
        verbose_name="Código do episodio",
        validators=[MinLengthValidator(2), MaxLengthValidator(100)]
        ) # gets the code from the episode | string

    url = models.URLField( 
        verbose_name="URL do episodio", 
        blank=True, 
        null=True
        ) # url to the episode endpoint
    
    created = models.DateTimeField(verbose_name="Data de criação do episodio no banco de dados") # gets the creationg date for the episode from the database
    
    def __str__(self):
        return f"Nome: {self.name} Data estreia: {self.air_date} Codigo: {self.episode_code}"
