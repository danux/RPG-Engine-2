# -*- coding: utf-8 -*-
from operator import methodcaller
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from model_utils.managers import PassThroughManagerMixin, InheritanceQuerySetMixin, InheritanceManager


class NotificationProfile(models.Model):
    """
    Class linking notifications to users.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='notification_profile')

    @property
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


class PassThroughInheritanceManager(PassThroughManagerMixin, InheritanceManager):
    pass


class NotificationQuerySet(InheritanceQuerySetMixin):
    """
    Manages the Notification model and all its children
    """
    def filter_unseen(self):
        """
        Returns unseen messages.
        """
        return self.filter(date_seen__isnull=True)

    def set_as_seen(self):
        """
        Sets all Notifications as seen.
        """
        map(methodcaller('set_as_seen'), self.all())


class Notification(models.Model):
    """
    A notification is a message for a user.
    """
    notification_profile = models.ForeignKey(NotificationProfile, related_name='notifications')
    date_created = models.DateTimeField(auto_now_add=True)
    date_seen = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = PassThroughInheritanceManager.for_queryset_class(NotificationQuerySet)()

    def set_as_seen(self):
        """
        Sets the seen date as now.
        """
        self.date_seen = timezone.now()
        self.save()

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
