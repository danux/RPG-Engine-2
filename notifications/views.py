# -*- coding: utf-8 -*-
"""
API views for notifications.
"""
from __future__ import unicode_literals
import json
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy, reverse
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
        :type action: unicode
        :return:
        """
        notification = get_object_or_404(self.get_queryset(), pk=pk)
        data = {
            'pk': notification.pk,
            'render': notification.render(),
            'set_as_seen_url': reverse_lazy(
                'notification-set-as-seen',
                kwargs={'pk': notification.pk},
                request=request
            ),
        }
        return Response(data)

    @detail_route(methods=['post'])
    def set_as_seen(self, request, pk):
        try:
            pk = int(pk)
        except TypeError:
            raise ParseError
        notification = get_object_or_404(self.get_queryset(), pk=pk)
        notification.set_as_seen()
        return Response({'status': 'ok'})
