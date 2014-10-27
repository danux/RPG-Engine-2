# -*- coding: utf-8 -*-
"""
Tests process for creating a quest.
"""
from django.core.urlresolvers import reverse
from mock import patch, PropertyMock
from characters.models import Character
from characters.tests.utils import CharacterUtils
from characters.views import CharacterListView
from rpg_auth.tests.utils import CreateUserMixin
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
        self.assertTemplateUsed(response, 'quests/no_characters_available.html')


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

    @patch('characters.models.CharacterProfile.available_characters', new_callable=PropertyMock)
    def test_if_not_characters_available_show_another_template(self, patched_available_characters):
        """
        If the user has no available characters then a different template should be used.
        """
        patched_available_characters.return_value.count.return_value = 0
        response = self.client.get(reverse('quests:select_character', kwargs={'location_slug': self.location_1.slug}))
        self.assertTemplateUsed(response, 'quests/no_characters_available.html')
