# ~*~ coding: utf-8 ~*~
"""
Tests for the the registration form.
"""
from mock import patch

from django import forms
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from rpg_auth.views import UserCreateView


class RegistrationTestCaseStub(TestCase):
    """
    Base class that provides valid data for testing.
    """

    def setUp(self):
        super(RegistrationTestCaseStub, self).setUp()
        self.valid_data = {
            'pen_name': u'Pen Name',
            'email': u'test@example.com',
            'password': u'test-password',
            'password2': u'test-password',
        }


class UserCanCreateAccountTestCase(RegistrationTestCaseStub):
    """
    A user can create an account on the site.
    """

    def test_there_is_a_registration_form(self):
        """
        There must be a form that the user can signup on.
        """
        response = self.client.get(reverse('rpg_auth:register'))
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
        response = self.client.post(reverse('rpg_auth:register'), data=self.valid_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', 'pen_name', u'This field is required.')

    def test_not_providing_an_email_address_raises_error(self):
        """
        If the user does not provide an email address the form must display an error.
        """
        self.valid_data.__delitem__('email')
        response = self.client.post(reverse('rpg_auth:register'), data=self.valid_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', u'This field is required.')

    def test_not_providing_a_password_raises_an_error(self):
        """
        If a password is not provided the form must display an error.
        """
        self.valid_data.__delitem__('password')
        response = self.client.post(reverse('rpg_auth:register'), data=self.valid_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', 'password', u'This field is required.')

    def test_not_supplying_a_password2_raises_an_error(self):
        """
        If a matching password is not provided the form must display an error.
        """
        self.valid_data.__delitem__('password2')
        response = self.client.post(reverse('rpg_auth:register'), data=self.valid_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', u'This field is required.')

    def test_not_supplying_a_matching_password2_raises_an_error(self):
        """
        If a matching password is not provided the form must display an error.
        """
        self.valid_data['password2'] = 'different-password'
        response = self.client.post(reverse('rpg_auth:register'), data=self.valid_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'form', 'password', u'Your passwords did not match.')
        self.assertFormError(response, 'form', 'password2', u'Your passwords did not match.')

    def test_if_valid_data_supplied_a_user_is_created(self):
        """
        If valid data is provided a user is created.
        """
        response = self.client.post(reverse('rpg_auth:register'), data=self.valid_data)
        self.assertRedirects(response, reverse('rpg_auth:register_confirmation'))
        user = get_user_model().objects.get(email=self.valid_data['email'])
        self.assertFalse(user.is_active)


class SendingWelcomeEmailTestCase(RegistrationTestCaseStub):
    """
    Tests that users can activate their accounts.
    """

    @patch('uuid.uuid1')
    def test_users_can_generate_activation_key(self, patched_uuid1):
        """
        Tests that a UUID can be generated and saved on to a user for activation.
        """
        patched_uuid1.return_value = 'demo-uuid'
        user = get_user_model()()
        user.generate_activation_key()
        self.assertEquals(user.activation_key, 'demo-uuid')

    def test_user_can_be_sent_activation_email(self):
        """
        Once a user has an activation key it can be emailed to them.
        """
        class MocKRequest(object):
            """
            Mock request with valid is_secure method.
            """

            @staticmethod
            def is_secure():
                """
                Returns true.
                """
                return True

            @staticmethod
            def get_host():
                """
                Returns true.
                """
                return 'host'

        user = get_user_model()(activation_key='activation-key', email='test@example.com')
        user.send_welcome_email(request=MocKRequest())
        self.assertEquals(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEquals(email.subject, u'Welcome to SoJ!')
        self.assertEquals(email.to[0], 'test@example.com')

    @patch('rpg_auth.models.RpgUser.generate_activation_key')
    @patch('rpg_auth.models.RpgUser.send_welcome_email')
    def test_welcome_email_is_sent_to_user(self, patched_send_welcome_email, patched_generate_activation_key):
        """
        If valid data is provided a user is created.
        """
        self.client.post(reverse('rpg_auth:register'), data=self.valid_data)
        self.assertEquals(patched_generate_activation_key.call_count, 1)
        self.assertEquals(patched_send_welcome_email.call_count, 1)


class ActivationProcessTestCase(TestCase):
    """
    Tests that the activation process works
    """

    def setUp(self):
        super(ActivationProcessTestCase, self).setUp()
        self.uuid = '0482094a-584c-11e4-9331-000c29a5c706'
        self.user = get_user_model().objects.create_user(
            activation_key=self.uuid, email='test@example.com', password='password'
        )

    def test_can_get_a_user_by_activation_key(self):
        """
        Tests that there is a manager method that can get a user by the activation key.
        """
        user = get_user_model().objects.get_by_activation_key(self.uuid)
        self.assertEquals(user, self.user)

    def test_will_not_return_activated_users(self):
        """
        Tests that the manager does not return users that have already been activated.
        """
        self.user.is_active = True
        self.user.save()
        self.assertRaises(get_user_model().DoesNotExist, get_user_model().objects.get_by_activation_key, self.uuid)

    def test_can_access_activation_url(self):
        """
        Tests that a user's activation URL is accessible.
        """
        response = self.client.get(reverse('rpg_auth:activation', kwargs={'activation_key': self.uuid}))
        self.assertEquals(response.status_code, 200)

    @patch('rpg_auth.views.ActivateFormView.load_user')
    def test_invalid_uuid_raises_404(self, patched_load_user):
        """
        Tests that a user's activation URL is accessible.
        """
        patched_load_user.return_value = False
        response = self.client.get(reverse('rpg_auth:activation', kwargs={'activation_key': self.uuid}))
        self.assertEquals(response.status_code, 404)

    def test_posting_to_activation_activates_user(self):
        """
        A post to activation view will activate the user.
        """
        response = self.client.post(reverse('rpg_auth:activation', kwargs={'activation_key': self.uuid}))
        self.assertRedirects(response, reverse('rpg_auth:activation_confirmation'))
        user = get_user_model().objects.get(pk=self.user.pk)
        self.assertTrue(user.is_active)
        self.assertEquals(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEquals(email.subject, u'Your account has been activated!')
        self.assertEquals(email.to[0], self.user.email)
