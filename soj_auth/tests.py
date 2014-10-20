# ~*~ coding: utf-8 ~*~
"""
Tests for the soj_auth app.
"""
from django import forms
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from soj_auth.views import UserCreateView


class UserCanCreateAccountTestCase(TestCase):
    """
    A user can create an account on the site.
    """

    def setUp(self):
        super(UserCanCreateAccountTestCase, self).setUp()
        self.valid_data = {
            'pen_name': u'Pen Name',
            'email': u'test@example.com',
            'password': u'test-password',
            'password2': u'test-password',
        }

    def test_there_is_a_registration_form(self):
        """
        There must be a form that the user can signup on.
        """
        response = self.client.get(reverse('soj_auth:register'))
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['view'], UserCreateView)
        self.assertIsInstance(response.context['form'].fields['pen_name'], forms.CharField)
        self.assertIsInstance(response.context['form'].fields['email'], forms.CharField)
        self.assertIsInstance(response.context['form'].fields['password'], forms.CharField)
        self.assertIsInstance(response.context['form'].fields['password2'], forms.CharField)
        self.assertIsInstance(response.context['form'].fields['password'].widget, forms.PasswordInput)
        self.assertIsInstance(response.context['form'].fields['password2'].widget, forms.PasswordInput)

    def test_not_providing_a_pen_name_raises_error(self):
        """
        If the user does not provide an email address the form must display an error.
        """
        self.valid_data.__delitem__('pen_name')
        response = self.client.post(reverse('soj_auth:register'), data=self.valid_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', 'pen_name', u'This field is required.')

    def test_not_providing_an_email_address_raises_error(self):
        """
        If the user does not provide an email address the form must display an error.
        """
        self.valid_data.__delitem__('email')
        response = self.client.post(reverse('soj_auth:register'), data=self.valid_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', u'This field is required.')

    def test_not_providing_a_password_raises_an_error(self):
        """
        If a password is not provided the form must display an error.
        """
        self.valid_data.__delitem__('password')
        response = self.client.post(reverse('soj_auth:register'), data=self.valid_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', 'password', u'This field is required.')

    def test_not_supplying_a_password2_raises_an_error(self):
        """
        If a matching password is not provided the form must display an error.
        """
        self.valid_data.__delitem__('password2')
        response = self.client.post(reverse('soj_auth:register'), data=self.valid_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', u'This field is required.')

    def test_not_supplying_a_matching_password2_raises_an_error(self):
        """
        If a matching password is not provided the form must display an error.
        """
        self.valid_data['password2'] = 'different-password'
        response = self.client.post(reverse('soj_auth:register'), data=self.valid_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', 'password', u'Your passwords did not match.')
        self.assertFormError(response, 'form', 'password2', u'Your passwords did not match.')

    def test_if_valid_data_supplied_a_user_is_created(self):
        """
        If valid data is provided a user is created.
        """
        response = self.client.post(reverse('soj_auth:register'), data=self.valid_data)
        self.assertRedirects(response, reverse('soj_auth:register-confirmation'))
        user = get_user_model().objects.get(email=self.valid_data['email'])
        self.assertFalse(user.is_active)
