# -*- coding: utf-8 -*-
"""
Tests the private message profile model
"""
from django.contrib.auth import get_user_model
from freezegun import freeze_time
from rpg_auth.tests.utils import CreateUserMixin


class PrivateMessageModelTestCase(CreateUserMixin):
    """
    Basic tests that check users can send messages at the model level.
    """
    def setUp(self):
        super(PrivateMessageModelTestCase, self).setUp()
        self.user2 = get_user_model().objects.create_user(
            pen_name=u'User 2',
            password=u'password',
            email=u'user_2@example.com',
            is_active=True,
        )
        self.user3 = get_user_model().objects.create_user(
            pen_name=u'User 3',
            password=u'password',
            email=u'user_3@example.com',
            is_active=True,
        )
        self.message_text = u'Test message'

    def test_can_send_message_to_user(self):
        """
        Tests a message can be sent to another user.
        """
        received_message, sent_message = self.user.message_profile.send_message(
            message_profile=self.user2.message_profile, message=self.message_text
        )

        self.assertEquals(self.user2.message_profile.received_messages.count(), 1)
        self.assertEquals(self.user.message_profile.sent_messages.count(), 1)

        self.assertEquals(self.user2.message_profile.received_messages.all()[0], received_message)
        self.assertEquals(self.user.message_profile.sent_messages.all()[0], sent_message)

    def test_can_get_list_of_message_threads(self):
        """
        Tests that a list of message threads can be returned.
        """
        with freeze_time('2000-01-01'):
            self.user3.message_profile.send_message(
                message_profile=self.user.message_profile, message=self.message_text
            )
        with freeze_time('2000-01-02'):
            self.user2.message_profile.send_message(
                message_profile=self.user.message_profile, message=self.message_text
            )
        with freeze_time('2000-01-03'):
            self.user.message_profile.send_message(
                message_profile=self.user2.message_profile, message=self.message_text
            )
        threads = self.user.message_profile.get_message_threads()
        self.assertEquals(threads.count(), 2)

        self.assertEquals(threads[0].message_count, 2)
        self.assertEquals(threads[1].message_count, 1)
