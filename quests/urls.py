# -*- coding: utf -*-
"""
URLs for the characters app.
"""
from django.conf.urls import patterns, url
from quests.views import SelectLocationListView, SelectCharacterListView, QuestCreateView


urlpatterns = patterns(
    '',
    url(r'^create/select-location/$', SelectLocationListView.as_view(), name='select_location'),
    url(
        r'^create/(?P<location_slug>[\w-]+)/select-character/$',
        SelectCharacterListView.as_view(),
        name='select_character'
    ),
    url(
        r'^create/(?P<location_slug>[\w-]+)/(?P<character_pk>\d+)/$',
        QuestCreateView.as_view(),
        name='create_quest'
    ),
)
