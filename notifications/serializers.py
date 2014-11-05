# -*- coding: utf-8 -*-
"""
Serializers for the API
"""
from rest_framework import serializers
from notifications.models import Notification


class NotificationSerializer(serializers.HyperlinkedModelSerializer):


    class Meta:
        model = Notification
        fields = ['id', 'date_created', 'url']
