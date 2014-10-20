# -*- coding: utf-8 -*-
"""
Tests that user can create characters.
"""
from django import forms
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from characters.tests.utils import CharacterUtils
from characters.views import CharacterCreateView
from rpg_auth.tests.utils import CreateUserMixin


class CharacterCreationFormTestCase(CreateUserMixin):
    """
    Tests the form for creating a character.
    """

    fixtures = ['world-test-data.json']

    def test_character_creation_form_renders(self):
        """
        Tests that the character creation form can load
        """
        response = self.client.get(reverse('characters:create'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['form'].fields), 7)
        self.assertIsInstance(response.context['view'], CharacterCreateView)
        self.assertTrue(issubclass(response.context['view'].__class__, CreateView))
        self.assertIsInstance(response.context['form'].fields['name'], forms.CharField)
        self.assertIsInstance(response.context['form'].fields['home_town'], forms.ModelChoiceField)
        self.assertIsInstance(response.context['form'].fields['race'], forms.ModelChoiceField)
        self.assertIsInstance(response.context['form'].fields['physical_description'], forms.CharField)
        self.assertIsInstance(response.context['form'].fields['personality'], forms.CharField)
        self.assertIsInstance(response.context['form'].fields['skills'], forms.CharField)
        self.assertIsInstance(response.context['form'].fields['full_biography'], forms.CharField)
        self.assertIsInstance(response.context['form'].fields['full_biography'].widget, forms.Textarea)
        self.assertFalse(response.context['form'].fields['full_biography'].required)

    def test_user_must_be_logged_in_to_access_character_creation(self):
        """
        If a user is not logged in they must be redirected to the login page.
        """
        self.client.logout()
        response = self.client.get(reverse('characters:create'))
        self.assertRedirects(response, '{0}?next={1}'.format(reverse('rpg_auth:login'), reverse('characters:create')))

    def test_if_user_has_filled_slots_cannot_create_character(self):
        """
        If a user has filled their slots they cannot create a new character.
        """
        CharacterUtils.create_character(self.user)
        response = self.client.get(reverse('characters:create'))
        self.assertEquals(response.status_code, 404)

    def test_once_created_redirects_back_to_dashboard(self):
        """
        Once a character is created the user should be taken back to the dashboard
        """
        valid_data = {
            'name': 'Name',
            'home_town': 1,
            'race': 1,
            'physical_description': 'test',
            'personality': 'test',
            'skills': 'test',
            'full_biography': 'test',
        }
        response = self.client.post(reverse('characters:create'), data=valid_data, follow=True)
        self.assertRedirects(response, reverse('characters:dashboard'))
