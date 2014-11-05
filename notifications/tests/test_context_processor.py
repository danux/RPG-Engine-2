# -*- coding: utf-8 -*-
"""
A notification profile is associated to a user and provides meta data about their notifications.
"""
from mock import patch, PropertyMock
from notifications.context_processors import unseen_notifications
from rpg_auth.tests.utils import CreateUserMixin
from soj.tests.utils import MockRequest


class ContextProcessorTestCase(CreateUserMixin):
    """
    Tests that the notification profile model behaves correctly.
    """

    @patch('notifications.models.NotificationProfile.unseen_notifications')
    def test_context_processor_has_unseen_notifications(self, patched_unseen_notifications):
        """
        A context processor should returns the user's unseen notifications.
        """
        patched_unseen_notifications.__get__ = PropertyMock(return_value={'test': 'test'})
        mock_request = MockRequest()
        mock_request.user = self.user
        self.assertEquals(unseen_notifications(mock_request), {'unseen_notifications': {'test': 'test'}})

    def test_if_user_is_not_logged_in_returns_empty_list(self):
        """
        If the user is not logged in then no notifications should be returned.
        """
        mock_request = MockRequest()
        self.assertEquals(unseen_notifications(mock_request), {'unseen_notifications': []})
