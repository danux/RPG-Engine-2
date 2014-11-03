# -*- coding: utf-8 -*-
"""
Utils for quests.
"""
import uuid
from characters.models import Character
from quests.models import Quest
from world.models import Location


class QuestUtils(object):
    """
    Provides methods for testing the character model.
    """
    @staticmethod
    def create_quest(user, character, location=None):
        """
        Creates a quest

        :type user: RpgUser
        :type character: Character
        :type location: Location
        """
        if location is None:
            location = Location.objects.get(pk=1)
        quest = Quest(
            title=unicode(uuid.uuid1()),
            description=u'description'
        )
        quest.initialise(gm=user.quest_profile, location=location, first_post=u'First post', character=character)
        return quest
