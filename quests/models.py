# -*- coding: utf-8 -*-
"""
Models for the quests app. These models serve as the heart of the game mechanics, drawing
on all other apps to create the game.
"""
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models, IntegrityError
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.text import slugify
from characters.models import Character
from world.models import BaseWorldModel, Location


class QuestProfile(models.Model):
    """
    Quest profiles link users to quests.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='quest_profile')
    following_quests = models.ManyToManyField('Quest', related_name='followers')

    def follow_quest(self, quest):
        """
        Adds the given quest to the following_quests M2M if the user is not already
        following the quest.

        :type quest: Quest
        """
        self.following_quests.add(quest)

    def unfollow_quest(self, quest):
        """
        Unfollows the given quest.

        :type quest: Quest
        """
        self.following_quests.remove(quest)


def create_quest_profile(sender, **kwargs):
    """
    Catches users being created and creates a quest profile for the user.

    :type sender: RpgUser
    :type kwargs: {}
    """
    del sender
    if kwargs['created']:
        QuestProfile.objects.create(user=kwargs['instance'])
post_save.connect(create_quest_profile, sender=settings.AUTH_USER_MODEL)


class Quest(BaseWorldModel):
    """
    Quests are collections of posts that describe the actions of characters in the world.

    Characters can come and go from quests, but they can only be on one at a time.

    Quests take place in towns and a quest can move in to a new town.

    This information is all tracked and dislayed to the user in the style of a timeline.
    """
    title = models.CharField(max_length=100, unique=True)
    gm = models.ForeignKey(QuestProfile)
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

    def initialise(self, gm, first_post, location, character):
        """
        Initialises a new quest, setting the location, first character and first post.
        :type gm: QuestProfile
        :type first_post: unicode
        :type location: Location
        :type character: Character
        """
        self.gm = gm
        self.save()
        self.move_to_location(location)
        self.add_character(character)
        self.gm.follow_quest(self)
        Post.objects.create(quest=self, character=character, content=first_post, location=location)

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

        :type character: Character
        """
        if character in self.current_characters:
            raise IntegrityError('Character is already on a quest')
        QuestCharacter.objects.create(quest=self, character=character)

    def remove_character(self, character):
        """
        Removes a characters from a quest.

        :type character: Character
        """
        quest_character = self.questcharacter_set.get_active_for_character(character=character)
        quest_character.date_departed = timezone.now()
        quest_character.save()

    def get_absolute_url(self):
        """
        Absolute URL to the quest
        """
        return reverse('quests:quest_detail', kwargs={'slug': self.slug})

    def create_slug(self, slug):
        """
        Tries to find an available slug.
        :type slug: unicode
        """
        try:
            self.__class__.objects.get(slug=slug)
        except self.__class__.DoesNotExist:
            return slug
        else:
            return self.create_slug('-{0}'.format(slug))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Overrides the save method. If no slug is set, the title will be sluggified.
        :type force_insert: bool
        :type force_update: bool
        :type using: Database
        :type update_fields: [] | ()
        """
        if self.slug == '':
            self.slug = self.create_slug(slugify(self.title))
        return super(Quest, self).save(force_insert, force_update, using, update_fields)


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


class Post(models.Model):
    """
    Model representing a post on a quest. A quest is made up of posts.
    """
    content = models.TextField()
    quest = models.ForeignKey(Quest, related_name='posts')
    character = models.ForeignKey(Character, related_name='posts')
    location = models.ForeignKey(Location, related_name='posts')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
