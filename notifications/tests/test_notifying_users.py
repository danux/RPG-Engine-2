# -*- coding: utf-8 -*-
"""
A notification profile is associated to a user and provides meta data about their notifications.
"""
from django.utils import timezone
from freezegun import freeze_time
from mock import patch
from notifications.models import GenericNotification, Notification
from rpg_auth.tests.utils import CreateUserMixin


class NotificationInheritanceTestCase(CreateUserMixin):
    """
    Tests that the notification profile model behaves correctly.
    """
    def test_can_filter_notifications(self):
        """
        If a subclass of notification is created it should be available as a notification
        on the user's notification_profile
        """
        generic_notification = GenericNotification.objects.create(
            notification_profile=self.user.notification_profile,
            text='test'
        )
        self.assertEquals(self.user.notification_profile.notifications.select_subclasses().count(), 1)
        self.assertEquals(
            self.user.notification_profile.notifications.all().select_subclasses()[0], generic_notification
        )

    def test_can_get_unread_notifications(self):
        """
        Can get unseen notifications for a user.
        """
        seen_generic_notification = GenericNotification.objects.create(
            notification_profile=self.user.notification_profile,
            text='test',
            date_seen=timezone.now()
        )
        unseen_generic_notification = GenericNotification.objects.create(
            notification_profile=self.user.notification_profile,
            text='test'
        )
        self.assertTrue(
            unseen_generic_notification in
            self.user.notification_profile.notifications.filter_unseen().select_subclasses()
        )
        self.assertFalse(
            seen_generic_notification in
            self.user.notification_profile.notifications.filter_unseen().select_subclasses()
        )

    @patch('notifications.models.NotificationQuerySet.filter_unseen')
    def test_short_cut_to_unseen_on_profile(self, patched_filter_unseen):
        """
        The NotificationProfile should have a shortcut to the filter_unseen method.
        """
        self.user.notification_profile.unseen_notifications()
        self.assertEquals(patched_filter_unseen.call_count, 1)

    def test_render_must_be_implemented(self):
        """
        If the render method is not implemented on a sub-class the Notification class has a NotImplemented exception
        """
        self.assertRaises(NotImplementedError, Notification().render)

    def test_generic_notification_can_render(self):
        """
        The GenericNotification must be able to render.
        """
        generic_notification = GenericNotification.objects.create(
            notification_profile=self.user.notification_profile,
            text='Test',
        )
        self.assertEquals(generic_notification.render(), generic_notification.text)

    def test_must_be_short_cut_to_create_notification(self):
        """
        Notification profile must have a shortcut to send notifications.
        """
        generic_notification = self.user.notification_profile.send_notification(
            notification_model=GenericNotification,
            text='Test'
        )
        self.assertEquals(
            self.user.notification_profile.notifications.all().select_subclasses()[0], generic_notification
        )


class MarkAsSeenTestCase(CreateUserMixin):
    """
    Tests that a notification can be marked as read.
    """
    def setUp(self):
        super(MarkAsSeenTestCase, self).setUp()
        self.notification1 = Notification.objects.create(
            notification_profile=self.user.notification_profile
        )
        self.notification2 = Notification.objects.create(
            notification_profile=self.user.notification_profile
        )

    @freeze_time('2000-01-01T00:00:00+00:00')
    def test_can_mark_notification_as_seen(self):
        """
        Tests a notification can be set as seen.
        """
        self.notification1.set_as_seen()
        self.assertEquals(self.notification1.date_seen, timezone.now())

    @freeze_time('2000-01-01T00:00:00+00:00')
    @patch('notifications.models.Notification.set_as_seen')
    def test_can_mark_query_set_as_unseen(self, mock_set_as_seen):
        """
        A whole queryset should be able to be set as seen.
        """
        self.user.notification_profile.unseen_notifications.set_as_seen()
        self.assertEquals(mock_set_as_seen.call_count, 2)
