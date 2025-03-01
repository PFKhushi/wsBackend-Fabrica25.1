from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

from .models import Location, Character, Episode, Gender, Status

class LocationModelTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            id=1,
            name="Earth C-137",
            location_type="Planet",
            dimension="Dimension C-137",
            url="https://example.com/api/location/1",
            created=timezone.now()
        )

    def test_slug_generation(self):
        """Test that a slug is automatically generated."""
        self.assertEqual(self.location.slug, "earth-c-137")
        
    def test_str_representation(self):
        """Test the string representation of the Location model."""
        expected = f"Nome: Earth C-137 Tipo de localização: Planet Dimensão: Dimension C-137"
        self.assertEqual(str(self.location), expected)
        
    def test_name_min_length(self):
        """Test minimum length validator for name field."""
        location = Location(
            id=2,
            name="A",  # Too short
            location_type="Planet",
            dimension="Dimension C-137",
            created=timezone.now()
        )
        with self.assertRaises(ValidationError):
            location.full_clean()


class CharacterModelTest(TestCase):
    def setUp(self):
        # Create a location first
        self.origin_location = Location.objects.create(
            id=1,
            name="Earth C-137",
            location_type="Planet",
            dimension="Dimension C-137",
            created=timezone.now()
        )
        
        self.current_location = Location.objects.create(
            id=2,
            name="Citadel of Ricks",
            location_type="Space station",
            dimension="unknown",
            created=timezone.now()
        )
        
        # Create a character without episodes first
        self.character = Character.objects.create(
            id=1,
            name="Rick Sanchez",
            status=Status.ALIVE,
            species="Human",
            subspecies="Scientist",
            gender=Gender.MALE,
            origin=self.origin_location,
            location=self.current_location,
            image_url="https://example.com/rick.jpg",
            url="https://example.com/api/character/1",
            created=timezone.now()
        )
        
        # Create an episode separately
        self.episode = Episode.objects.create(
            id=1,
            name="Pilot",
            air_date=datetime.date(2013, 12, 2),
            episode_code="S01E01",
            created=timezone.now()
        )
        
        # Now add the episode to the character
        self.character.episode.add(self.episode)
        
    def test_slug_generation(self):
        """Test that a slug is automatically generated."""
        self.assertEqual(self.character.slug, "rick-sanchez")
        
    def test_str_representation(self):
        """Test the string representation of the Character model."""
        expected = f"Nome: Rick Sanchez Espécie: Human Subspécie: Scientist Gênero: M Estado: A Origem: Nome: Earth C-137 Tipo de localização: Planet Dimensão: Dimension C-137 Localização atual: Nome: Citadel of Ricks Tipo de localização: Space station Dimensão: unknown"
        self.assertEqual(str(self.character), expected)
        
    def test_character_episode_relationship(self):
        """Test that a character can be associated with episodes."""
        self.assertEqual(self.character.episode.count(), 1)
        self.assertEqual(self.character.episode.first(), self.episode)
        
    def test_character_default_gender(self):
        """Test default gender value."""
        character = Character.objects.create(
            id=2,
            name="Test Character",
            species="Test Species",
            created=timezone.now()
        )
        self.assertEqual(character.gender, Gender.UNKNOWN)
        
    def test_character_default_status(self):
        """Test default status value."""
        character = Character.objects.create(
            id=3,
            name="Test Character",
            species="Test Species",
            created=timezone.now()
        )
        self.assertEqual(character.status, Status.UNKNOWN)


class EpisodeModelTest(TestCase):
    def setUp(self):
        self.episode = Episode.objects.create(
            id=1,
            name="Pilot",
            air_date=datetime.date(2013, 12, 2),
            episode_code="S01E01",
            created=timezone.now()
        )
        
    def test_slug_generation(self):
        """Test that a slug is automatically generated."""
        self.assertEqual(self.episode.slug, "pilot")
        
    def test_str_representation(self):
        """Test the string representation of the Episode model."""
        expected = f"Nome: Pilot Data estreia: 2013-12-02 Codigo: S01E01"
        self.assertEqual(str(self.episode), expected)
        
    def test_character_relationship(self):
        """Test that episodes can have characters."""
        # Create a character first, then add the episode
        character = Character.objects.create(
            id=1,
            name="Rick Sanchez",
            status=Status.ALIVE,
            species="Human",
            created=timezone.now()
        )
        
        # Now add the episode to the character
        character.episode.add(self.episode)
        
        self.assertEqual(character.episode.count(), 1)
        self.assertEqual(character.episode.first(), self.episode)


class SlugModelTest(TestCase):
    """
    Tests for the SlugModel abstract base class.
    Using Location model as a concrete implementation for testing.
    """
    def test_custom_slug_source(self):
        """
        Test manually setting a slug for a model instance.
        """
        # Create a location with an explicit slug
        location = Location.objects.create(
            id=99,
            name="Test Location",
            location_type="Test Type",
            dimension="Test Dimension",
            slug="custom-slug",  # Explicitly set slug
            created=timezone.now()
        )
        
        # Check that our custom slug was used
        self.assertEqual(location.slug, "custom-slug")
        
    def test_slug_generated_from_name(self):
        """Test that slug is generated from name by default."""
        location = Location.objects.create(
            id=100,
            name="Test Location Two",
            location_type="Test Type",
            dimension="Test Dimension",
            created=timezone.now()
        )
        
        self.assertEqual(location.slug, "test-location-two")
        
    def test_slug_uniqueness(self):
        """Test handling of duplicate slugs."""
        # Create first location
        location1 = Location.objects.create(
            id=101,
            name="Earth",
            location_type="Planet",
            dimension="Dimension C-137",
            created=timezone.now()
        )
        
        # Create second location with same name but explicitly set a different slug
        location2 = Location.objects.create(
            id=102,
            name="Earth",
            location_type="Planet",
            dimension="Dimension C-500",
            slug="earth-2",  # Manually set a unique slug
            created=timezone.now()
        )
        
        self.assertEqual(location1.slug, "earth")
        self.assertEqual(location2.slug, "earth-2")