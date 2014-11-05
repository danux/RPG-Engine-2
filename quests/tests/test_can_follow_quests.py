# -*- coding: utf-8 -*-
"""
Tests that quests can be followed by users. This will be key to driving timelines.
"""
from braces.views import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from mock import patch
from characters.tests.utils import CharacterUtils
from quests.mixins import QuestFromRequestMixin
from quests.tests.utils import QuestUtils
from rpg_auth.tests.utils import CreateUserMixin


class CanFollowQuestTestCase(CreateUserMixin):
    """
    Test profile allows following quests.
    """
    fixtures = ['world-test-data.json']

    def setUp(self):
        super(CanFollowQuestTestCase, self).setUp()
        self.character = CharacterUtils.create_character(self.user)
        self.quest = QuestUtils.create_quest(self.user, self.character)
        self.follower_user = get_user_model().objects.create_user(
            pen_name=u'Follower',
            password=u'password',
            email=u'follower@example.com',
            is_active=True,
        )

    def test_profile_can_follow_quests(self):
        """
        Tests that a quest can be given to a quest profile to follow.
        """
        self.assertEquals(self.follower_user.quest_profile.following_quests.count(), 0)
        self.follower_user.quest_profile.follow_quest(self.quest)
        self.assertEquals(self.follower_user.quest_profile.following_quests.count(), 1)

    def test_cannot_follow_quest_twice(self):
        """
        Tests a user can only follow a quest once.
        """
        self.follower_user.quest_profile.follow_quest(self.quest)
        self.follower_user.quest_profile.follow_quest(self.quest)
        self.assertEquals(self.follower_user.quest_profile.following_quests.count(), 1)

    def test_user_can_unfollow_quest(self):
        """
        Tests that a user can unfollow a quest.
        """
        self.follower_user.quest_profile.follow_quest(self.quest)
        self.follower_user.quest_profile.unfollow_quest(self.quest)
        self.assertEquals(self.follower_user.quest_profile.following_quests.count(), 0)

    def test_when_initialising_quest_auto_follows(self):
        """
        When a user creates a quest they must auto follow it
        """
        self.assertEquals(self.user.quest_profile.following_quests.count(), 1)


class CanFollowQuestViewsTestCase(CreateUserMixin):
    """
    Test views can be used to follow quests.
    """
    fixtures = ['world-test-data.json']

    def setUp(self):
        super(CanFollowQuestViewsTestCase, self).setUp()
        self.gm_user = get_user_model().objects.create_user(
            pen_name=u'GM',
            password=u'password',
            email=u'gm@example.com',
            is_active=True,
        )
        self.character = CharacterUtils.create_character(self.gm_user)
        self.quest = QuestUtils.create_quest(self.gm_user, self.character)

    def test_view_renders(self):
        """
        Test the view to follow a quest renders.
        """
        response = self.client.get(reverse('quests:follow_quest', kwargs={'quest_slug': self.quest.slug}))
        self.assertEquals(response.status_code, 200)
        self.assertTrue(issubclass(response.context['view'].__class__, FormView))
        self.assertTrue(issubclass(response.context['view'].__class__, LoginRequiredMixin))
        self.assertTrue(issubclass(response.context['view'].__class__, QuestFromRequestMixin))
        self.assertTemplateUsed(response, 'quests/follow_quest.html')

    @patch('quests.models.QuestProfile.follow_quest')
    def test_posting_to_form_follows_quest(self, patched_follow_quest):
        """
        Submitting the form should follow the quest.
        """
        response = self.client.post(
            reverse('quests:follow_quest', kwargs={'quest_slug': self.quest.slug}),
            follow=True
        )
        self.assertRedirects(response, self.quest.get_absolute_url())
        patched_follow_quest.assert_called_once_with(quest=self.quest)
        message = list(response.context['messages'])[0]
        self.assertEqual('You are now following {0}!'.format(self.quest.title), unicode(message.message))
        self.assertTrue('success' in message.tags)


class CanUnFollowQuestViewsTestCase(CreateUserMixin):
    """
    Test views can be used to unfollow quests.
    """
    fixtures = ['world-test-data.json']

    def setUp(self):
        super(CanUnFollowQuestViewsTestCase, self).setUp()
        self.gm_user = get_user_model().objects.create_user(
            pen_name=u'GM',
            password=u'password',
            email=u'gm@example.com',
            is_active=True,
        )
        self.character = CharacterUtils.create_character(self.gm_user)
        self.quest = QuestUtils.create_quest(self.gm_user, self.character)
        self.user.quest_profile.follow_quest(quest=self.quest)

    def test_view_renders(self):
        """
        Test the view to unfollow a quest renders.
        """
        response = self.client.get(reverse('quests:unfollow_quest', kwargs={'quest_slug': self.quest.slug}))
        self.assertEquals(response.status_code, 200)
        self.assertTrue(issubclass(response.context['view'].__class__, FormView))
        self.assertTrue(issubclass(response.context['view'].__class__, LoginRequiredMixin))
        self.assertTrue(issubclass(response.context['view'].__class__, QuestFromRequestMixin))
        self.assertTemplateUsed(response, 'quests/unfollow_quest.html')

    @patch('quests.models.QuestProfile.unfollow_quest')
    def test_posting_to_form_unfollows_quest(self, patched_unfollow_quest):
        """
        Submitting the form should unfollow the quest.
        """
        response = self.client.post(
            reverse('quests:unfollow_quest', kwargs={'quest_slug': self.quest.slug}),
            follow=True
        )
        self.assertRedirects(response, self.quest.get_absolute_url())
        patched_unfollow_quest.assert_called_once_with(quest=self.quest)
        message = list(response.context['messages'])[0]
        self.assertEqual('You are no longer following {0}!'.format(self.quest.title), unicode(message.message))
        self.assertTrue('success' in message.tags)
