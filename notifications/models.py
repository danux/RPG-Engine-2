# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from model_utils.managers import InheritanceManager


class NotificationProfile(models.Model):
    """
    Class linking notifications to users.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='notification_profile')

    def unseen_notifications(self):
        """
        Returns the user's unseen notifications.
        """
        return self.notifications.filter_unseen().select_subclasses()

    def send_notification(self, notification_model, **kwargs):
        """
        Adds a notification to the notification profile.
        :type notification_model: Notification
        :type kwargs: {}
        """
        return notification_model.objects.create(notification_profile=self, **kwargs)


def create_notification_profile(sender, **kwargs):
    """
    Catches users being created and creates a notification profile for the user.

    :type sender: RpgUser
    :type kwargs: {}
    """
    del sender
    if kwargs['created']:
        NotificationProfile.objects.create(user=kwargs['instance'])
post_save.connect(create_notification_profile, sender=settings.AUTH_USER_MODEL)


class NotificationManager(InheritanceManager):
    """
    Manages the Notification model and all its children
    """
    def filter_unseen(self):
        """
        Returns unseen messages.
        """
        return self.filter(date_seen__isnull=True)


class Notification(models.Model):
    """
    A notification is a message for a user.
    """
    notification_profile = models.ForeignKey(NotificationProfile, related_name='notifications')
    date_created = models.DateTimeField(auto_now_add=True)
    date_seen = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = NotificationManager()

    def render(self):
        """
        Renders the notification
        :rtype: unicode
        """
        raise NotImplementedError('Notification must be sub-classed and you must implement a render method')


class GenericNotification(Notification):
    """
    A generic notification that simply contains text.
    """
    text = models.TextField()

    def render(self):
        """
        Renders the notification
        :rtype: unicode
        """
        return self.text
