# -*- coding: utf-8 -*-
"""
Tests that the createsuperuser command will work.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from mock import patch


class SuperUserTestCase(TestCase):
    """
    Tests can createsuperuser
    """
    @patch('rpg_auth.models.RpgUserManager._create_user')
    def test_super_user(self, patched_create_user):
        """
        Tests user created is a superuser.
        """
        user_model = get_user_model()
        options = {
            'email': 'superuser@example.com',
            'pen_name': 'SuperUser',
            'password': 'password',
        }
        user_model.objects.create_superuser(**options)
        patched_create_user.assert_called_once_with(
            **dict(options.items() + dict(is_superuser=True, is_staff=True).items())
        )
