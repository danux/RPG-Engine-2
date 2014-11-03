# -*- coding: utf-8 -*-
"""
Tests that the character dashboard renders
"""
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from characters.tests.utils import CharacterUtils
from characters.views import CharacterListView
from rpg_auth.tests.utils import CreateUserMixin


class CharacterDashboardTestCase(CreateUserMixin):
    """
    Tests the form for creating a character.
    """

    fixtures = ['world-test-data.json']

    def test_character_dashboard_renders(self):
        """
        Tests that the character creation form can load
        """
        response = self.client.get(reverse('characters:dashboard'))
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['view'], CharacterListView)
        self.assertTrue(issubclass(response.context['view'].__class__, ListView))

    def test_user_must_be_logged_in_to_access_character_dashboard(self):
        """
        If a user is not logged in they must be redirected to the login page.
        """
        self.client.logout()
        response = self.client.get(reverse('characters:dashboard'))
        self.assertRedirects(
            response,
            '{0}?next={1}'.format(reverse('rpg_auth:login'), reverse('characters:dashboard'))
        )

    def test_only_logged_in_users_characters_are_shown(self):
        """
        Only the logged in user's characters should be shown.
        """
        second_user = get_user_model().objects.create_user(
            pen_name='Pen Name 2',
            password='password',
            email='test 2@example.com',
            is_active=True,
        )
        other_character = CharacterUtils.create_character(second_user)
        my_character = CharacterUtils.create_character(self.user)
        response = self.client.get(reverse('characters:dashboard'))
        self.assertIn(my_character, response.context['object_list'])
        self.assertNotIn(other_character, response.context['object_list'])
