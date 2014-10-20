# ~*~ coding: utf ~*~
"""
Master URLs file for SoJ.
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^auth/', include('rpg_auth.urls', namespace='rpg_auth')),
    url(r'^characters/', include('characters.urls', namespace='characters')),
    url(r'^admin/', include(admin.site.urls)),
)
