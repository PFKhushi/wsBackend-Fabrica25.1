from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Location, Character, Episode, Gender, Status

# Create your tests here.

class LocationModelTest(TestCase):
    def test_location_creation(self):
        # Create a Location instance
        location = Location.objects.create(
            id=1,
            name="Earth",
            location_type="Planet",
            dimension="C-137",
            url="https://rickandmortyapi.com/api/location/1"
        )

        # Test fields
        self.assertEqual(location.name, "Earth")
        self.assertEqual(location.location_type, "Planet")
        self.assertEqual(location.dimension, "C-137")
        self.assertEqual(location.url, "https://rickandmortyapi.com/api/location/1")

        # Test slug generation
        self.assertEqual(location.slug, "earth")

        # Test string representation
        self.assertEqual(str(location), "Nome: Earth Tipo de localização: Planet Dimensão: C-137")

    def test_location_validation(self):
        # Test MinLengthValidator for name
        with self.assertRaises(ValidationError):
            location = Location(name="A", location_type="Planet", dimension="C-137")
            location.full_clean()  # Triggers validation

        # Test MaxLengthValidator for name
        with self.assertRaises(ValidationError):
            location = Location(name="A" * 101, location_type="Planet", dimension="C-137")
            location.full_clean()
            
class CharacterModelTest(TestCase):
    def setUp(self):
        # Create a Location for testing relationships
        self.location = Location.objects.create(
            id=1,
            name="Earth",
            location_type="Planet",
            dimension="C-137"
        )

    def test_character_creation(self):
        # Create a Character instance
        character = Character.objects.create(
            id=1,
            name="Rick Sanchez",
            status=Status.ALIVE,
            species="Human",
            subspecies="Genius",
            gender=Gender.MALE,
            origin=self.location,
            location=self.location,
            image_url="https://rickandmortyapi.com/api/character/avatar/1.jpeg",
            url="https://rickandmortyapi.com/api/character/1"
        )

        # Test fields
        self.assertEqual(character.name, "Rick Sanchez")
        self.assertEqual(character.status, Status.ALIVE)
        self.assertEqual(character.species, "Human")
        self.assertEqual(character.subspecies, "Genius")
        self.assertEqual(character.gender, Gender.MALE)
        self.assertEqual(character.origin, self.location)
        self.assertEqual(character.location, self.location)
        self.assertEqual(character.image_url, "https://rickandmortyapi.com/api/character/avatar/1.jpeg")
        self.assertEqual(character.url, "https://rickandmortyapi.com/api/character/1")

        # Test slug generation
        self.assertEqual(character.slug, "rick-sanchez")

        # Test string representation
        self.assertEqual(str(character), "Nome: Rick Sanchez Espécie: Human Subspécie: Genius Gênero: M Estado: A Origem: Earth Localização atual: Earth")

    def test_character_validation(self):
        # Test MinLengthValidator for name
        with self.assertRaises(ValidationError):
            character = Character(name="R", status=Status.ALIVE, species="Human")
            character.full_clean()

        # Test MaxLengthValidator for name
        with self.assertRaises(ValidationError):
            character = Character(name="R" * 101, status=Status.ALIVE, species="Human")
            character.full_clean()

class EpisodeModelTest(TestCase):
    def setUp(self):
        # Create a Character for testing relationships
        self.location = Location.objects.create(
            id=1,
            name="Earth",
            location_type="Planet",
            dimension="C-137"
        )
        self.character = Character.objects.create(
            id=1,
            name="Rick Sanchez",
            status=Status.ALIVE,
            species="Human",
            origin=self.location,
            location=self.location
        )

    def test_episode_creation(self):
        # Create an Episode instance
        episode = Episode.objects.create(
            id=1,
            name="Pilot",
            air_date="2013-12-02",
            episode_code="S01E01",
            url="https://rickandmortyapi.com/api/episode/1"
        )
        episode.characters.add(self.character)

        # Test fields
        self.assertEqual(episode.name, "Pilot")
        self.assertEqual(str(episode.air_date), "2013-12-02")
        self.assertEqual(episode.episode_code, "S01E01")
        self.assertEqual(episode.url, "https://rickandmortyapi.com/api/episode/1")

        # Test slug generation
        self.assertEqual(episode.slug, "s01e01")

        # Test relationships
        self.assertEqual(episode.characters.count(), 1)
        self.assertEqual(episode.characters.first(), self.character)

        # Test string representation
        self.assertEqual(str(episode), "Nome: Pilot Data estreia: 2013-12-02 Codigo: S01E01")

    def test_episode_validation(self):
        # Test MinLengthValidator for name
        with self.assertRaises(ValidationError):
            episode = Episode(name="P", air_date="2013-12-02", episode_code="S01E01")
            episode.full_clean()

        # Test MaxLengthValidator for name
        with self.assertRaises(ValidationError):
            episode = Episode(name="P" * 101, air_date="2013-12-02", episode_code="S01E01")
            episode.full_clean()