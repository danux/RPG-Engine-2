# -*- coding: utf-8 -*-
"""
Utils that provide useful starting points for tests.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase


class CreateUserMixin(TestCase):
    """
    Mixin that comes with a user, ready to login and use.
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            pen_name=u'Pen Name',
            password=u'password',
            email=u'test@example.com',
            is_active=True,
        )
        self.client.login(username=self.user.email, password='password')
