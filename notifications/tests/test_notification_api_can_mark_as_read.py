# -*- coding: utf-8 -*-
"""
Tests that notifications can be marked as read through the API.
"""
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from mock import patch
from notifications.models import GenericNotification, Notification
from rpg_auth.tests.utils import CreateUserMixin


class MarkAsReadTestCase(CreateUserMixin):
    """
    Tests that notifications can be marked as read through the API.
    """
    def setUp(self):
        super(MarkAsReadTestCase, self).setUp()
        self.user.notification_profile.send_notification(GenericNotification, text='Test')
        self.notification = Notification.objects.all().select_subclasses().get(pk=1)
        self.set_as_notified_url = reverse('notification-set-as-seen', kwargs={'pk': self.notification.pk})

    @patch('notifications.models.Notification.set_as_seen')
    def test_can_set_as_notified(self, patched_set_as_seen):
        """
        Tests a notification can be set as notified
        """
        self.client.post(self.set_as_notified_url)
        self.assertEquals(patched_set_as_seen.call_count, 1)

    def test_404_if_already_unseen(self):
        """
        If a notification has already been set as seen then it should 404.
        """
        self.notification.set_as_seen()
        response = self.client.post(self.set_as_notified_url)
        self.assertEquals(response.status_code, 404)

    def test_can_only_set_own_as_seen(self):
        """
        A user should only be allowed to set their own messages as unseen.
        """
        self.client.logout()
        get_user_model().objects.create_user(
            pen_name='pen name 2', email='other_user@example.com', password='password', is_active=True
        )
        self.client.login(username='other_user@example.com', password='password')
        response = self.client.post(self.set_as_notified_url)
        self.assertEquals(response.status_code, 404)
