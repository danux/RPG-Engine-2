# -*- coding: utf-8 -*-
"""
Tests how quests relate to other models. For example, tracking a quest through locations,
or which characters have come and gone from quests.

Quests must be able to provide
"""
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time
from mock import PropertyMock, patch
from characters.tests.utils import CharacterUtils
from quests.models import Quest
from world.models import Location


class QuestToLocationRelationshipTestCase(TestCase):
    """
    Tests that quests can be tracked through locations.
    """
    fixtures = ['world-test-data.json']

    def setUp(self):
        super(QuestToLocationRelationshipTestCase, self).setUp()
        self.location1 = Location.objects.get(pk=1)
        self.location2 = Location.objects.get(pk=2)
        self.quest = Quest.objects.create(name='Quest')

    def test_quest_can_be_in_location(self):
        """
        Tests that a quest can be in a location.
        """
        self.quest.move_to_location(self.location1)
        self.assertEquals(self.quest.current_location, self.location1)

    def test_raise_integrity_error_if_quest_already_in_location(self):
        """
        Defensive check that if a quest is already in a location it cannot be moved there.
        """
        self.quest.move_to_location(self.location1)
        self.assertRaises(IntegrityError, self.quest.move_to_location, self.location1)

    @freeze_time('2000-01-01 00:00:00')
    def test_when_leaving_location_date_recorded(self):
        """
        When moving to a new location the datetime the old location was left
        should be recorded.
        """
        self.quest.move_to_location(self.location1)
        self.quest.move_to_location(self.location2)
        quest_location1 = self.quest.questlocation_set.all()[0]
        quest_location2 = self.quest.questlocation_set.all()[1]
        self.assertEquals(timezone.now(), quest_location1.date_departed)
        self.assertIsNone(quest_location2.date_departed)

    def test_location_can_get_current_quests(self):
        """
        A location knows the quests that are currently taking places there.
        """
        quest1 = Quest.objects.create(name='Quest 1', slug='quest-1')
        quest2 = Quest.objects.create(name='Quest 2', slug='quest-2')
        quest3 = Quest.objects.create(name='Quest 3', slug='quest-3')
        quest1.move_to_location(self.location1)
        quest2.move_to_location(self.location1)
        quest3.move_to_location(self.location1)
        quest3.move_to_location(self.location2)
        self.assertEquals(list(self.location1.current_quests), [quest1, quest2])
        self.assertEquals(list(self.location2.current_quests), [quest3])

    def test_location_can_get_former_quests(self):
        """
        A location knows the quests that are currently taking places there.
        """
        quest1 = Quest.objects.create(name='Quest 1', slug='quest-1')
        quest2 = Quest.objects.create(name='Quest 2', slug='quest-2')
        quest3 = Quest.objects.create(name='Quest 3', slug='quest-3')
        quest1.move_to_location(self.location1)
        quest1.move_to_location(self.location2)
        quest2.move_to_location(self.location1)
        quest3.move_to_location(self.location2)
        self.assertEquals(list(self.location1.former_quests), [quest1])


class QuestToCharacterRelationshipTestCase(TestCase):
    """
    Tests the relationship between quests and characters.

    Multiple characters can be on a quest at any one time and a character can only be
    on one quest at a time.
    """
    fixtures = ['world-test-data.json']

    def setUp(self):
        super(QuestToCharacterRelationshipTestCase, self).setUp()

        self.quest1 = Quest.objects.create(name='Quest 1', slug='quest-1')
        self.quest2 = Quest.objects.create(name='Quest 2', slug='quest-2')

        self.user1 = get_user_model().objects.create_user(
            pen_name='Test User 1',
            email="test1@example.com",
            password="password"
        )
        self.character1 = CharacterUtils.create_character(self.user1)
        self.character2 = CharacterUtils.create_character(get_user_model().objects.create_user(
            pen_name='Test User 2',
            email="test2@example.com",
            password="password"
        ))
        self.character3 = CharacterUtils.create_character(self.user1)

    def test_character_can_join_quests(self):
        """
        Tests that a character can join a quest and the quest knows the current characters.
        """
        self.quest1.add_character(self.character1)
        self.quest1.add_character(self.character2)
        self.assertEquals(list(self.quest1.current_characters), [self.character1, self.character2])

    def test_characters_can_leave_quests(self):
        """
        A character can join a quest and leave it.
        """
        self.quest1.add_character(self.character1)
        self.quest1.add_character(self.character2)
        self.quest1.remove_character(self.character1)
        self.assertEquals(list(self.quest1.current_characters), [self.character2])
        self.assertEquals(list(self.quest1.former_characters), [self.character1])

    def test_raise_integrity_error_if_character_already_on_quest(self):
        """
        Defensive check that if a character is already on a quest they cannot be added again.
        """
        self.quest1.add_character(self.character1)
        self.assertRaises(IntegrityError, self.quest1.add_character, self.character1)

    def test_character_profile_can_get_available_characters(self):
        """
        A method must be available on the character profile model that returns
        characters not currently on a quest.
        """
        self.quest1.add_character(self.character1)
        self.quest1.add_character(self.character3)
        self.quest1.remove_character(self.character3)
        self.assertEquals(list(self.user1.character_profile.available_characters), [self.character3])

    def test_character_is_available_after_leaving_quest(self):
        """
        A method must be available on the character profile model that returns
        characters not currently on a quest.
        """
        self.quest1.add_character(self.character1)
        self.quest1.remove_character(self.character1)
        self.assertEquals(
            list(self.user1.character_profile.available_characters), [self.character1, self.character3]
        )

    def test_character_knows_current_quest(self):
        """
        Tests that a character know its current quest.
        """
        self.assertIsNone(self.character1.current_quest)
        self.quest1.add_character(self.character1)
        self.assertEquals(self.character1.current_quest, self.quest1)
        self.quest1.remove_character(self.character1)
        self.assertIsNone(self.character1.current_quest)

    @patch('characters.models.CharacterProfile.available_characters', new_callable=PropertyMock)
    def test_character_profile_knows_if_has_available(self, patched_available_characters):
        """
        There should be a boolean on the character profile to return True if
        the user has available characters.
        """
        patched_available_characters.return_value.count.return_value = 1
        self.assertTrue(self.user1.character_profile.has_available_characters)
        patched_available_characters.return_value.count.return_value = 0
        self.assertFalse(self.user1.character_profile.has_available_characters)
