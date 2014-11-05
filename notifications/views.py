# -*- coding: utf-8 -*-
"""
API views for notifications.
"""
from __future__ import unicode_literals
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    model = Notification

    def get_queryset(self):
        return self.request.user.notification_profile.unseen_notifications

    def list(self, request):
        serializer = NotificationSerializer(self.get_queryset(), many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        :param request:
        :type pk: int
        :return:
        """
        try:
            notification = get_object_or_404(self.get_queryset(), pk=int(pk))
        except ValueError:
            raise ParseError
        serializer = NotificationSerializer(notification, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def set_as_seen(self, request, pk):
        del request
        try:
            pk = int(pk)
        except TypeError:
            raise ParseError
        notification = get_object_or_404(self.get_queryset(), pk=pk)
        notification.set_as_seen()
        return Response({'status': 'ok'})
