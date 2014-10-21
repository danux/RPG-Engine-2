# -*- coding: utf-8 -*-
"""
Models for the quests app. These models serve as the heart of the game mechanics, drawing
on all other apps to create the game.
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError
from django.utils import timezone
from characters.models import Character
from world.models import BaseWorldModel, Location


class Quest(BaseWorldModel):
    """
    Quests are collections of posts that describe the actions of characters in the world.

    Characters can come and go from quests, but they can only be on one at a time.

    Quests take place in towns and a quest can move in to a new town.

    This information is all tracked and dislayed to the user in the style of a timeline.
    """
    title = models.CharField(max_length=100)
    locations = models.ManyToManyField(Location, through='QuestLocation')
    characters = models.ManyToManyField(Character, through='QuestCharacter')

    @property
    def current_location(self):
        """
        Gets the current Location by the one with the most recent date_created.
        :return: Location
        """
        current_quest_location = self.current_quest_location
        return None if current_quest_location is None else current_quest_location.location

    @property
    def current_quest_location(self):
        """
        Gets the current Location by the one with the most recent date_created.
        """
        try:
            return self.questlocation_set.get_active()
        except ObjectDoesNotExist:
            return None

    def move_to_location(self, location):
        """
        Moves a quest to a new location.
        :param location: The Location to move the quest to.
        :type location: Location
        """
        current_quest_location = self.current_quest_location
        if current_quest_location is not None:
            if location == current_quest_location.location:
                raise IntegrityError()
            current_quest_location.date_departed = timezone.now()
            current_quest_location.save()
        QuestLocation.objects.create(quest=self, location=location)

    @property
    def current_characters(self):
        """
        Gets characters currently on the quest.
        """
        return self.characters.filter_active()

    @property
    def former_characters(self):
        """
        Gets characters that have left the quest.
        """
        return self.characters.filter_departed()

    def add_character(self, character):
        """
        Adds a character to a quest.
        """
        if character in self.current_characters:
            raise IntegrityError('Character is already on a quest')
        QuestCharacter.objects.create(quest=self, character=character)

    def remove_character(self, character):
        """
        Removes a characters from a quest.
        """
        quest_character = self.questcharacter_set.get_active_for_character(character=character)
        quest_character.date_departed = timezone.now()
        quest_character.save()


class BaseQuestRelationManager(models.Manager):
    """
    Manager for BaseQuestRelation and its subclasses.
    """
    def get_active_for_character(self, character):
        """
        Returns active object for a character.
        :type character: Character
        """
        return self.get(date_departed__isnull=True, character=character)

    def get_active(self):
        """
        Gets a single active instance.
        """
        return self.get(date_departed__isnull=True)


class BaseQuestRelation(models.Model):
    """
    Base class for classes holding through relationships for quests.
    """
    quest = models.ForeignKey(Quest)
    date_created = models.DateTimeField(auto_now_add=True)
    date_departed = models.DateTimeField(null=True, blank=True)

    objects = BaseQuestRelationManager()

    class Meta(object):
        """
        Meta properties
        """
        abstract = True


class QuestLocation(BaseQuestRelation):
    """
    Holds the relationship between quests and towns.
    """
    location = models.ForeignKey(Location)


class QuestCharacter(BaseQuestRelation):
    """
    Holds the relationship between quests and characters.
    """
    character = models.ForeignKey(Character)
