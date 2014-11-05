# -*- coding: utf-8 -*-
"""
Tests that notifications can be marked as read through the API.
"""
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from notifications.models import GenericNotification, Notification
from rpg_auth.tests.utils import CreateUserMixin


class MarkAsReadTestCase(CreateUserMixin):
    """
    Tests that notifications can be marked as read through the API.
    """
    def setUp(self):
        super(MarkAsReadTestCase, self).setUp()
        self.user.notification_profile.send_notification(
            GenericNotification,
            text='Test'
        )
        self.notification = Notification.objects.all().select_subclasses().get(pk=1)
        self.set_as_notified_url = reverse(
            'api:mark_notification_as_read',
            kwargs={'api_name': 'v1', 'resource_name': 'notification', 'pk': self.notification.pk}
        )

    def test_can_set_as_notified(self):
        """
        Tests a notification can be set as notified
        """
        response = self.client.post(self.set_as_notified_url)
        self.assertEquals(response.status_code, 200)
        notification = Notification.objects.all().select_subclasses().get(pk=1)
        self.assertIsNotNone(notification.date_seen)

    def test_404_if_already_unseen(self):
        """
        If a notification has already been set as seen then it should 404.
        """
        self.notification.set_as_seen()
        response = self.client.post(self.set_as_notified_url)
        self.assertEquals(response.status_code, 404)

    def test_can_only_modify_set_own_as_seen(self):
        """
        A user should only be allowed to set their own messages as unseen.
        """
        get_user_model().objects.create_user(email='other_user@example.com', password='password')
        response = self.client.login(username='other_user@example.com', password='password')
        self.assertEquals(response.status_code, 403)
