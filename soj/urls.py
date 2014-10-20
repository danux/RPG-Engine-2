# ~*~ coding: utf ~*~
"""
Master URLs file for SoJ.
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^auth/', include('soj_auth.urls', namespace='soj_auth')),
    url(r'^admin/', include(admin.site.urls)),
)
