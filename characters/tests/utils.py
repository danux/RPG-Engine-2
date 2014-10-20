# -*- coding: utf-8 -*-
"""
Utils for characters.
"""
import uuid
from characters.models import Character
from world.models import Location, Race


class CharacterUtils(object):
    """
    Provides methods for testing the character model.
    """
    @staticmethod
    def create_character(user):
        """
        Creates a character

        :type user: RpgUser
        """
        return Character.objects.create(
            name=unicode(uuid.uuid1()),
            character_profile=user.character_profile,
            home_town=Location.objects.get(pk=1),
            race=Race.objects.get(pk=1)
        )
