# -*- coding: utf -*-
"""
Master URLs file for RPG Engine.
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from notifications import views

router = routers.DefaultRouter()
router.register(r'notifications', views.NotificationViewSet)


urlpatterns = patterns(
    '',
    url(r'^auth/', include('rpg_auth.urls', namespace='rpg_auth')),
    url(r'^characters/', include('characters.urls', namespace='characters')),
    url(r'^world/', include('world.urls', namespace='world')),
    url(r'^quest/', include('quests.urls', namespace='quests')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)
