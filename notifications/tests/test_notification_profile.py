# -*- coding: utf-8 -*-
"""
A notification profile is associated to a user and provides meta data about their notifications.
"""
from notifications.models import NotificationProfile
from rpg_auth.tests.utils import CreateUserMixin


class NotificationProfileCreationTestCase(CreateUserMixin):
    """
    Tests that the notification profile model behaves correctly.
    """
    def test_creating_user_creates_notification_profile(self):
        """
        Tests notification profiles are created.
        """
        self.assertIsInstance(self.user.notification_profile, NotificationProfile)
