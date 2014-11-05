# -*- coding: utf-8 -*-
"""
Serializers for the API
"""
from rest_framework import serializers
from rest_framework.fields import Field
from notifications.models import Notification


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    rendered = Field(source='render')

    class Meta(object):
        model = Notification
        fields = ['id', 'date_created', 'rendered', 'url']
