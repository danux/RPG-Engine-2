# -*- coding: utf-8 -*-
"""
A quest profile is associated to a user and provides meta data about their quests.
"""
from quests.models import QuestProfile
from rpg_auth.tests.utils import CreateUserMixin


class QuestProfileCreation(CreateUserMixin):
    """
    Tests that the quest profile model behaves correctly.
    """
    def test_creating_user_creates_quest_profile(self):
        """
        Tests quest profiles are created.
        """
        self.assertIsInstance(self.user.quest_profile, QuestProfile)
