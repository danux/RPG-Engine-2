# -*- coding: utf-8 -*-
"""
API views for notifications.
"""
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          mixins.UpdateModelMixin,
                          GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
