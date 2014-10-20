# -*- coding: utf -*-
"""
URLs for the world app.
"""
from django.conf.urls import patterns, url
from world.views import ContinentDetailView, ContinentListView, LocationDetailView


urlpatterns = patterns(
    '',
    url(r'^/$', ContinentListView.as_view(), name='continent_list'),
    url(r'^continent/(?P<slug>[\w-]+)/$', ContinentDetailView.as_view(), name='continent_detail'),
    url(r'^location/(?P<slug>[\w-]+)/$', LocationDetailView.as_view(), name='location_detail'),
)
