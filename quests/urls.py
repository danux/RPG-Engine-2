# -*- coding: utf -*-
"""
URLs for the characters app.
"""
from django.conf.urls import patterns, url
from quests.views import SelectLocationListView, SelectCharacterListView, QuestCreateView, QuestDetailView, \
    PostCreateView


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
    url(
        r'^(?P<slug>[\w-]+)/$',
        QuestDetailView.as_view(),
        name='quest_detail'
    ),
    url(
        r'^(?P<quest_slug>[\w-]+)/post/$',
        PostCreateView.as_view(),
        name='create_post'
    ),
)
