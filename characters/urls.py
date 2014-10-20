# ~*~ coding: utf ~*~
"""
URLs for the auth app.
"""
from django.conf.urls import patterns, url

from characters.views import CharacterCreateView


urlpatterns = patterns(
    '',
    url(r'^create/$', CharacterCreateView.as_view(), name='create'),
)
