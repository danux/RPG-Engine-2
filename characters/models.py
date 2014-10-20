# ~*~ coding: utf ~*~
"""
Characters are owned by users and participate within the game.
"""
from django.conf import settings
from django.db import models

from world.models import Race, Location


class Character(models.Model):
    """
    Model representing a character in the world.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=50)
    home_town = models.ForeignKey(Location)
    race = models.ForeignKey(Race)
    physical_description = models.CharField(max_length=500)
    personality = models.CharField(max_length=500)
    skills = models.CharField(max_length=500)
    full_biography = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
