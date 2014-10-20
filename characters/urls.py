# ~*~ coding: utf ~*~
"""
URLs for the auth app.
"""
from django.conf.urls import patterns, url

from characters.views import CharacterCreateView, CharacterListView


urlpatterns = patterns(
    '',
    url(r'^/$', CharacterListView.as_view(), name='dashboard'),
    url(r'^create/$', CharacterCreateView.as_view(), name='create'),
)
