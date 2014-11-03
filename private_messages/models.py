# -*- coding: utf-8 -*-
"""
Private message models
"""
from django.conf import settings
from django.db import models
from django.db.models import Count, Max
from django.db.models.signals import post_save


class MessageProfile(models.Model):
    """
    Message profile is associated to a user and stores meta data about
    a user's message options.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='message_profile')

    def send_message(self, message_profile, message):
        """
        Sends a message to another user

        :type message_profile: MessageProfile
        :type message: unicode

        :rtype: list[PrivateMessage]
        """
        # See if there is currently a thread for the receiver.
        receiver_thread, _ = message_profile.threads.get_or_create(other_message_profile=self)
        received_message = PrivateMessage.objects.create(
            sender=self,
            message_thread=receiver_thread,
            message=message
        )

        # The sender's version
        sender_thread, _ = self.threads.get_or_create(other_message_profile=message_profile)
        sent_message = PrivateMessage.objects.create(
            sender=self,
            message_thread=sender_thread,
            message=message
        )
        return received_message, sent_message

    def get_message_threads(self):
        """
        Returns a user's message threads. A message thread is message aggregates by the sender.
        """
        return self.threads.annotate(
            message_count=Count('messages'), last_updated=Max('messages__date_created')
        ).order_by(
            '-last_updated'
        )

    @property
    def received_messages(self):
        """
        Returns all messages received by the user.

        :rtype: QuerySet
        """
        return PrivateMessage.objects.filter(message_thread__owner=self).exclude(sender=self)

    @property
    def sent_messages(self):
        """
        Returns all messages sent by the user.

        :rtype: QuerySet
        """
        return PrivateMessage.objects.filter(message_thread__owner=self, sender=self)


def create_message_profile(sender, **kwargs):
    """
    Catches users being created and creates a profile for the user.

    :type sender: RpgUser
    :type kwargs: {}
    """
    del sender
    if kwargs['created']:
        MessageProfile.objects.create(user=kwargs['instance'])
post_save.connect(create_message_profile, sender=settings.AUTH_USER_MODEL)


class MessageThread(models.Model):
    """
    A message thread is a conversation between 2 users.
    """
    owner = models.ForeignKey(MessageProfile, related_name='threads', db_index=True)
    other_message_profile = models.ForeignKey(MessageProfile, related_name='other_message_profile', db_index=True)


class PrivateMessage(models.Model):
    """
    Model representing a message from one user to another.
    """
    message_thread = models.ForeignKey(MessageThread, related_name='messages')
    sender = models.ForeignKey(MessageProfile, db_index=True)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
