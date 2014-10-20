# -*- coding: utf-8 -*-
"""
World models. These models define the game universe and are reference by all
other aspects of the game.
"""
from django.db import models


class BaseWorldModel(models.Model):
    """
    Provides common fields to all world models.
    """
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta(object):
        """
        Sets model to abstract
        """
        abstract = True


class Race(BaseWorldModel):
    """
    Races are used by characters and define much of the physical appearance.
    """


class Continent(BaseWorldModel):
    """
    A continent represents a land-body within the world and is made up of locations.
    """


class Location(BaseWorldModel):
    """
    A location is a place in the world. They can be home towns, or the location of quests.
    """
    continent = models.ForeignKey(Continent)

    @property
    def current_quests(self):
        """
        References the reverse relation of quests.
        """
        return self.quest_set.filter(questlocation__date_departed__isnull=True)

    @property
    def former_quests(self):
        """
        Returns the former quests from a location.
        """
        return self.quest_set.filter(questlocation__date_departed__isnull=False)
