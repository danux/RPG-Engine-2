# ~*~ coding: utf-8 ~*~
"""
Tests that user can create characters.
"""
from django import forms
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from characters.views import CharacterCreateView


class CharacterCreationFormTestCase(TestCase):
    """
    Tests the form for creating a character.
    """

    def setUp(self):
        super(CharacterCreationFormTestCase, self).setUp()
        self.user = get_user_model().objects.create(
            pen_name=u'Pen Name',
            password=u'password',
            email=u'test@example.com'
        )
        self.client.login(username=self.user.email, password='password')

    def test_character_creation_form_renders(self):
        """
        Tests that the character creation form can load
        """
        response = self.client.get(reverse('characters:create'))
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['view'], CharacterCreateView)
        self.assertIsInstance(response.context['form'].fields['name'], forms.CharField)
        self.assertIsInstance(response.context['form'].fields['home_town'], forms.ModelChoiceField)
        self.assertIsInstance(response.context['form'].fields['race'], forms.ModelChoiceField)
        self.assertIsInstance(response.context['form'].fields['physical_description'], forms.CharField)
        self.assertIsInstance(response.context['form'].fields['personality'], forms.CharField)
        self.assertIsInstance(response.context['form'].fields['skills'], forms.CharField)
        self.assertIsInstance(response.context['form'].fields['full_biography'], forms.CharField)
        self.assertIsInstance(response.context['form'].fields['full_biography'].widget, forms.Textarea)
