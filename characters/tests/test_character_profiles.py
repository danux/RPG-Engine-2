# -*- coding: utf-8 -*-
"""
A character profile is associated to a user and provides meta data about their characters
and their options regarding characters.
"""
from characters.models import CharacterProfile
from characters.tests.utils import CharacterUtils
from rpg_auth.tests.utils import CreateUserMixin


class CharacterProfileCreation(CreateUserMixin):
    """
    Tests that the character profile model behaves correctly.
    """
    def test_creating_user_creates_character_profile(self):
        """
        Tests that the character creation form can load
        """
        self.assertIsInstance(self.user.character_profile, CharacterProfile)


class CharacterProfileTests(CreateUserMixin):
    """
    Tests the attributes and methods on the CharacterProfile behave as expected.
    """
    fixtures = ['world-test-data.json']

    def test_profile_knows_number_of_characters(self):
        """
        A CharacterProfile should know the number of characters a user has.
        """
        self.assertEquals(self.user.character_profile.character_count, 0)
        CharacterUtils.create_character(self.user)
        self.assertEquals(self.user.character_profile.character_count, 1)
        CharacterUtils.create_character(self.user)
        self.assertEquals(self.user.character_profile.character_count, 2)

    def test_profile_knows_if_user_can_have_more_characters(self):
        """
        A CharacterProfile should know the number of characters a user has.
        """
        self.user.character_profile.slots = 1
        self.assertTrue(self.user.character_profile.has_free_slot)
        CharacterUtils.create_character(self.user)
        self.assertFalse(self.user.character_profile.has_free_slot)
        self.user.character_profile.slots = 2
        self.assertTrue(self.user.character_profile.has_free_slot)
