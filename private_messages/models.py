# -*- coding: utf-8 -*-
"""
Private message models
"""
from django.conf import settings
from django.db import models
from django.db.models import Count, Max
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from notifications.models import Notification


class MessageNotification(Notification):
    """
    A message notification informs a user there is a new message in a thread.
    """
    private_message = models.ForeignKey('PrivateMessage')

    def render(self):
        """
        Renders the notification.
        """
        return render_to_string(
            'private_messages/notifications/message_notification.html', {'private_message': self.private_message}
        )


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
        received_message, sent_message = PrivateMessage.objects.create_private_message(
            from_message_profile=self,
            to_message_profile=message_profile,
            message=message
        )
        try:
            message_notification = self.user.notification_profile.unseen_notifications.get(
                messagenotification__private_message__message_thread=received_message.message_thread
            )
        except Notification.DoesNotExist:
            self.user.notification_profile.send_notification(
                MessageNotification, private_message=received_message
            )
        else:
            message_notification.private_message = received_message
            message_notification.save()
        return received_message, sent_message

    @property
    def message_threads(self):
        """
        Returns a user's message threads. A message thread is message aggregates by the sender.
        """
        return self.threads.filter_message_thread_list()

    @property
    def received_messages(self):
        """
        Returns all messages received by the user.

        :rtype: QuerySet
        """
        return PrivateMessage.objects.filter_received_by_message_profile(message_profile=self)

    @property
    def sent_messages(self):
        """
        Returns all messages sent by the user.

        :rtype: QuerySet
        """
        return PrivateMessage.objects.filter_sent_by_message_profile(message_profile=self)


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


class MessageThreadManager(models.Manager):
    """
    Managers the MessageThread model
    """
    def filter_message_thread_list(self):
        """
        Prepares the threads for listing to the user. Annotates the number
        of messages in the thread and orders by the last post date in the thread.
        """
        return self.annotate(
            message_count=Count('messages'), last_updated=Max('messages__date_created')
        ).order_by(
            '-last_updated'
        )


class MessageThread(models.Model):
    """
    A message thread is a conversation between 2 users.
    """
    owner = models.ForeignKey(MessageProfile, related_name='threads', db_index=True)
    other_message_profile = models.ForeignKey(MessageProfile, related_name='other_message_profile', db_index=True)

    objects = MessageThreadManager()


class PrivateMessageManager(models.Manager):
    """
    Managers the PrivateMessage model
    """
    def create_private_message(self, from_message_profile, to_message_profile, message):
        """
        Creates a private message. First, it will look for a thread between the from user
        and the to user. If the thread does not exist it will be created for both users.
        The message will then be duplicated in to both threads so both users retain a copy.

        :type from_message_profile: MessageProfile
        :type to_message_profile: MessageProfile
        :type message: unicode
        :return: list[MessageProfile]
        """
        # The receiver's version
        receiver_thread, _ = to_message_profile.threads.get_or_create(other_message_profile=from_message_profile)
        received_message = self.create(
            sender=from_message_profile,
            message_thread=receiver_thread,
            message=message
        )

        # The sender's version
        sender_thread, _ = from_message_profile.threads.get_or_create(other_message_profile=to_message_profile)
        sent_message = self.create(
            sender=from_message_profile,
            message_thread=sender_thread,
            message=message
        )
        return received_message, sent_message

    def filter_received_by_message_profile(self, message_profile):
        """
        Returns all received messages (regardless of thread) for a given user.

        :type message_profile: MessageProfile
        """
        return self.filter(message_thread__owner=message_profile).exclude(sender=message_profile)

    def filter_sent_by_message_profile(self, message_profile):
        """
        Returns all sent message for a given user.

        :type message_profile: MessageProfile
        """
        return self.filter(message_thread__owner=message_profile, sender=message_profile)


class PrivateMessage(models.Model):
    """
    Model representing a message from one user to another.
    """
    message_thread = models.ForeignKey(MessageThread, related_name='messages')
    sender = models.ForeignKey(MessageProfile, db_index=True)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    objects = PrivateMessageManager()
