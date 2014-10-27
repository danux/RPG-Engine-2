# -*- coding: utf -*-
"""
URLs for the characters app.
"""
from django.conf.urls import patterns, url
from quests.views import SelectLocationListView, SelectCharacterListView


urlpatterns = patterns(
    '',
    url(r'^create/select-location/$', SelectLocationListView.as_view(), name='select_location'),
    url(
        r'^create/(?P<location_slug>[\w-]+)/select-character/$',
        SelectCharacterListView.as_view(),
        name='select_character'
    ),
)
