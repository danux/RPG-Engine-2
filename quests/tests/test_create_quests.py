# -*- coding: utf-8 -*-
"""
Tests process for creating a quest.
"""
from braces.views import LoginRequiredMixin
from django import forms
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from mock import patch, PropertyMock
from characters.mixins import NoAvailableCharactersMixin
from characters.models import Character
from characters.tests.utils import CharacterUtils
from characters.views import CharacterListView
from quests.models import Quest, Post
from rpg_auth.tests.utils import CreateUserMixin
from world.mixins import LocationFromRequestMixin
from world.models import Location
from world.views import ContinentListView


class SelectLocationTestCase(CreateUserMixin):
    """
    Tests that users can create quests
    """
    fixtures = ['world-test-data.json']

    def setUp(self):
        super(SelectLocationTestCase, self).setUp()
        self.character_1 = CharacterUtils.create_character(self.user)

    def test_view_to_select_location_renders(self):
        """
        A view must exist allowing a user to select a location to quest in.
        """
        response = self.client.get(reverse('quests:select_location'))
        self.assertEquals(response.status_code, 200)
        self.assertTrue(issubclass(response.context['view'].__class__, ContinentListView))
        self.assertTemplateUsed(response, 'quests/select_location.html')

    def test_user_must_be_logged_in_to_select_location(self):
        """
        A user must be logged in to select the location of a quest.
        """
        self.client.logout()
        response = self.client.get(reverse('quests:select_location'))
        self.assertRedirects(response, '{0}?next={1}'.format(
            reverse('rpg_auth:login'), reverse('quests:select_location')
        ))

    @patch('characters.models.CharacterProfile.available_characters', new_callable=PropertyMock)
    def test_if_not_characters_available_show_another_template(self, patched_available_characters):
        """
        If the user has no available characters then a different template should be used.
        """
        patched_available_characters.return_value.count.return_value = 0
        response = self.client.get(reverse('quests:select_location'))
        self.assertTemplateUsed(response, 'characters/no_characters_available.html')


class SelectCharacterTestCase(CreateUserMixin):
    """
    Tests that if the user has selected a location they can also select a character.
    """
    fixtures = ['world-test-data.json']

    def setUp(self):
        super(SelectCharacterTestCase, self).setUp()
        self.location_1 = Location.objects.get(pk=1)
        self.character_1 = CharacterUtils.create_character(self.user)
        self.character_2 = CharacterUtils.create_character(self.user)

    def test_view_to_select_character_renders(self):
        """
        Tests that given a valid location, a user's characters are listed.
        """
        response = self.client.get(reverse('quests:select_character', kwargs={'location_slug': self.location_1.slug}))
        self.assertEquals(response.status_code, 200)
        self.assertTrue(issubclass(response.context['view'].__class__, CharacterListView))
        self.assertTemplateUsed(response, 'quests/select_character.html')
        self.assertEquals(response.context['location'], self.location_1)

    def test_invalid_location_gives_404(self):
        """
        Tests if an invalid location is given a 404 is raised.
        """
        response = self.client.get(reverse('quests:select_character', kwargs={'location_slug': 'fake-slug'}))
        self.assertEquals(response.status_code, 404)

    @patch('characters.models.CharacterProfile.available_characters', new_callable=PropertyMock)
    def test_object_list_is_only_available_characters(self, patched_available_characters):
        """
        The object list should only contain characters that are available.
        """
        available_characters = Character.objects.filter(pk=1)
        patched_available_characters.return_value = available_characters
        response = self.client.get(reverse('quests:select_character', kwargs={'location_slug': self.location_1.slug}))
        self.assertEquals(response.context['object_list'], available_characters)
        self.assertTrue(self.character_2 not in response.context['object_list'])

    @patch('characters.models.CharacterProfile.has_available_characters', new_callable=PropertyMock)
    def test_if_not_characters_available_show_another_template(self, patched_has_available_characters):
        """
        If the user has no available characters then a different template should be used.
        """
        patched_has_available_characters.return_value = False
        response = self.client.get(reverse('quests:select_character', kwargs={'location_slug': self.location_1.slug}))
        self.assertTemplateUsed(response, 'characters/no_characters_available.html')


class CreateQuestTestCase(CreateUserMixin):
    """
    Tests that a quest can be created once a user has selected the location and the character to start.
    """
    fixtures = ['world-test-data.json']

    def setUp(self):
        super(CreateQuestTestCase, self).setUp()
        self.location_1 = Location.objects.get(pk=1)
        self.character_1 = CharacterUtils.create_character(self.user)
        self.character_2 = CharacterUtils.create_character(self.user)

    def test_create_view_renders(self):
        """
        The view to create a quest should render.
        """
        response = self.client.get(
            reverse(
                'quests:create_quest',
                kwargs={'location_slug': self.location_1.slug, 'character_pk': self.character_1.pk},
            )
        )
        self.assertEquals(response.status_code, 200)
        self.assertTrue(issubclass(response.context['view'].__class__, CreateView))
        self.assertTrue(issubclass(response.context['view'].__class__, NoAvailableCharactersMixin))
        self.assertTrue(issubclass(response.context['view'].__class__, LocationFromRequestMixin))
        self.assertTrue(issubclass(response.context['view'].__class__, LoginRequiredMixin))
        self.assertTemplateUsed(response, 'quests/quest_form.html')
        self.assertEquals(response.context['location'], self.location_1)
        self.assertEquals(response.context['character'], self.character_1)
        self.assertEquals(len(response.context['form'].fields), 3)

        self.assertIsInstance(response.context['form'].fields['title'], forms.CharField)
        self.assertTrue(response.context['form'].fields['title'].required)

        self.assertIsInstance(response.context['form'].fields['description'], forms.CharField)
        self.assertIsInstance(response.context['form'].fields['description'].widget, forms.Textarea)
        self.assertTrue(response.context['form'].fields['description'].required)

        self.assertIsInstance(response.context['form'].fields['first_post'], forms.CharField)
        self.assertIsInstance(response.context['form'].fields['first_post'].widget, forms.Textarea)
        self.assertTrue(response.context['form'].fields['first_post'].required)

    def test_invalid_character_gives_404(self):
        """
        If an invalid PK is provided for a character a 404 error is returned.
        """
        response = self.client.get(
            reverse(
                'quests:create_quest',
                kwargs={'location_slug': self.location_1.slug, 'character_pk': 999},
            )
        )
        self.assertEquals(response.status_code, 404)

    @patch('characters.models.CharacterProfile.available_characters', new_callable=PropertyMock)
    def test_unavailable_character_gives_404(self, patched_available_characters):
        """
        If another user's character is provided then a 404 should be raised.
        """
        patched_available_characters.return_value = Character.objects.filter(pk=self.character_1.pk)
        response = self.client.get(
            reverse(
                'quests:create_quest',
                kwargs={'location_slug': self.location_1.slug, 'character_pk': self.character_2.pk},
            )
        )
        self.assertEquals(response.status_code, 404)

    def test_quests_have_initialise_method(self):
        """
        Quests should have an initialise method that sets the character, location
        and the GM.
        """
        quest = Quest(title=u'Title', description=u'description')
        quest.initialise(
            gm=self.user.quest_profile,
            first_post=u'first post',
            location=self.location_1,
            character=self.character_1,
        )
        self.assertEquals(quest.gm, self.user.quest_profile)
        self.assertTrue(self.character_1 in quest.current_characters)
        self.assertEqual(self.location_1, quest.current_location)
        post = Post.objects.get(pk=1)
        self.assertEquals(self.character_1, post.character)
        self.assertEquals(self.location_1, post.location)
        self.assertEquals(u'first post', post.content)

    def test_creating_a_quest_sets_first_post_characters_and_location(self):
        """
        When a quest is created the logged in user should be set as the GM.
        """
        valid_data = {
            'title': u'Title 1',
            'description': u'Description 1',
            'first_post': u'first post',
        }
        response = self.client.post(
            reverse(
                'quests:create_quest',
                kwargs={'location_slug': self.location_1.slug, 'character_pk': self.character_1.pk},
            ),
            data=valid_data,
            follow=True,
        )
        quest = Quest.objects.get(pk=1)
        self.assertRedirects(response, quest.get_absolute_url())
        self.assertEquals(quest.gm, self.user.quest_profile)
        self.assertTrue(self.character_1 in quest.current_characters)
        self.assertEqual(self.location_1, quest.current_location)
        post = Post.objects.get(pk=1)
        self.assertEquals(quest, post.quest)
        self.assertEquals(self.character_1, post.character)
        self.assertEquals(self.location_1, post.location)
        self.assertEquals(u'first post', post.content)


class QuestDetailViewTestCase(CreateUserMixin):
    """
    Tests that there is a detail view for quests.
    """
    fixtures = ['world-test-data.json']

    def test_detail_view_renders(self):
        """
        It should be possible to view a quest.
        """
        quest = Quest.objects.create(
            title=u'title', description=u'description', slug=u'slug', gm=self.user.quest_profile
        )
        response = self.client.get(reverse('quests:quest_detail', kwargs={'slug': quest.slug},))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], quest)
