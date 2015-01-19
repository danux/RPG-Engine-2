# -*- coding: utf-8 -*-
"""
Tests that users can have characters join a quest.
"""
from braces.views import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from mock import patch
from characters.mixins import AvailableCharacterFromRequestMixin, NoAvailableCharactersMixin, CharacterFromRequestMixin
from characters.tests.utils import CharacterUtils
from quests.mixins import QuestFromRequestMixin
from quests.models import Quest
from rpg_auth.tests.utils import CreateUserMixin
from world.models import Location


class JoinQuestTestCase(CreateUserMixin):
    """
    Tests that users can join quests.
    """
    fixtures = ['world-test-data.json']

    def setUp(self):
        super(JoinQuestTestCase, self).setUp()
        self.character_1 = CharacterUtils.create_character(self.user)
        self.location_1 = Location.objects.get(pk=1)

        self.user_1 = get_user_model().objects.create(email='test1@example.com', pen_name='Test 1')
        self.character_2 = CharacterUtils.create_character(self.user_1)
        self.quest = Quest(title=u'Quest')
        self.quest.initialise(
            gm=self.user_1.quest_profile, first_post=u'First post', character=self.character_2, location=self.location_1
        )

    def test_can_render_join_view(self):
        """
        Tests that the view to join a quest renders.
        """
        response = self.client.get(
            reverse('quests:join_quest', kwargs={'quest_slug': self.quest.slug, 'character_pk': self.character_1.pk})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTrue(issubclass(response.context['view'].__class__, FormView))
        self.assertTrue(issubclass(response.context['view'].__class__, LoginRequiredMixin))
        self.assertTrue(issubclass(response.context['view'].__class__, QuestFromRequestMixin))
        self.assertTrue(issubclass(response.context['view'].__class__, AvailableCharacterFromRequestMixin))
        self.assertTrue(issubclass(response.context['view'].__class__, NoAvailableCharactersMixin))
        self.assertTemplateUsed(response, 'quests/join_quest.html')

    @patch('quests.models.Quest.add_character')
    def test_posting_to_form_joins_quest(self, patched_follow_quest):
        """
        Submitting the form should follow the quest.
        """
        response = self.client.post(
            reverse('quests:join_quest', kwargs={'quest_slug': self.quest.slug, 'character_pk': self.character_1.pk}),
            follow=True
        )
        self.assertRedirects(response, self.quest.get_absolute_url())
        patched_follow_quest.assert_called_once_with(character=self.character_1)
        message = list(response.context['messages'])[0]
        self.assertEqual(
            '{0} has joined {1}!'.format(self.character_1.name, self.quest.title), unicode(message.message)
        )
        self.assertTrue('success' in message.tags)
