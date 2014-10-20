# -*- coding: utf -*-
"""
Characters are owned by users and participate within the game.
"""
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from world.models import Race, Location


class CharacterProfile(models.Model):
    """
    Character profile is associated to a user and stores meta data about
    a user's character options.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='character_profile')
    slots = models.IntegerField(default=1)

    @property
    def character_count(self):
        """
        Returns the number of characters a user has.

        :return: int -- the number of characters a user has.
        """
        return self.character_set.count()

    @property
    def has_free_slot(self):
        """
        Returns True if the user's character count is fewer than the number of
        slots the user has
        """
        return self.character_count < self.slots

    @property
    def available_characters(self):
        """
        Returns characters not currently on quests.
        """
        return self.character_set.filter_available()


def create_character_profile(sender, **kwargs):
    """
    Catches users being created and creates a character profile for the user.

    :type sender: RpgUser
    :type kwargs: {}
    """
    del sender
    if kwargs['created']:
        CharacterProfile.objects.create(user=kwargs['instance'])
post_save.connect(create_character_profile, sender=settings.AUTH_USER_MODEL)


class CharacterManager(models.Manager):
    """
    Manager methods for characters.
    """
    def filter_available(self):
        """
        Returns characters not currently on a quest.
        """
        return self.filter(
            Q(questcharacter__date_departed__isnull=False) | Q(questcharacter__isnull=True)
        )


class Character(models.Model):
    """
    Model representing a character in the world.
    """
    character_profile = models.ForeignKey(CharacterProfile)
    name = models.CharField(max_length=50, unique=True)
    home_town = models.ForeignKey(Location)
    race = models.ForeignKey(Race)
    physical_description = models.CharField(max_length=500)
    personality = models.CharField(max_length=500)
    skills = models.CharField(max_length=500)
    full_biography = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    objects = CharacterManager()

    def __unicode__(self):
        return self.name

    @property
    def current_quest(self):
        """
        Returns the characters current quest
        :return: Quest
        """
        try:
            return self.quest_set.get(questcharacter__date_departed__isnull=True)
        except ObjectDoesNotExist:
            return None
