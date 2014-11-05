# -*- coding: utf-8 -*-
"""
Tests private message notifications.
"""
from django.contrib.auth import get_user_model
from mock import patch
from rpg_auth.tests.utils import CreateUserMixin


class PrivateMessageModelTestCase(CreateUserMixin):
    """
    Basic tests that check users can send messages at the model level.
    """
    def setUp(self):
        super(PrivateMessageModelTestCase, self).setUp()
        self.user2 = get_user_model().objects.create_user(
            pen_name='User 2',
            password='password',
            email='user_2@example.com',
            is_active=True,
        )
        self.message_text = 'A message that is longer than 30 characters and should be truncated in the notification'

    def test_notification_sent_for_message(self):
        """
        Tests a message can be sent to another user.
        """
        received_message, _ = self.user.message_profile.send_message(
            message_profile=self.user2.message_profile, message=self.message_text
        )
        self.assertEquals(self.user.notification_profile.unseen_notifications[0].private_message, received_message)

    def test_notification_not_sent_twice_if_unread_for_thread(self):
        """
        If a new private message is added to a thread but there is already a notification about a previous message
        then the notification should be updated.
        """
        _, _ = self.user.message_profile.send_message(
            message_profile=self.user2.message_profile, message=self.message_text
        )
        received_message, _ = self.user.message_profile.send_message(
            message_profile=self.user2.message_profile, message=self.message_text
        )
        self.assertEquals(self.user.notification_profile.unseen_notifications.count(), 1)
        self.assertEquals(self.user.notification_profile.unseen_notifications[0].private_message, received_message)

    @patch('private_messages.models.render_to_string')
    def test_notification_renders(self, mocked_render_to_string):
        """
        Tests the notification renders correctly.
        """
        received_message, _ = self.user.message_profile.send_message(
            message_profile=self.user2.message_profile, message=self.message_text
        )
        self.user.notification_profile.unseen_notifications[0].render()
        mocked_render_to_string.assert_called_once_with(
            'private_messages/notifications/message_notification.html', {'private_message': received_message}
        )
