# -*- coding: utf-8 -*-
"""
Mixins that can be used for classes that need some default world objects behaviour.
"""
from django.shortcuts import get_object_or_404
from world.models import Location


class LocationFromRequestMixin(object):
    """
    Loads the location specified by location_slug and adds it to the context.

    If the location is invalid then a 404 is raised.
    """
    location_queryset = Location.objects.all()

    def __init__(self):
        super(LocationFromRequestMixin, self).__init__()
        self.location_slug = None

    def dispatch(self, request, *args, **kwargs):
        """
        Adds the location to self.
        :param request: HttpRequest
        :param args: []
        :param kwargs: {}
        :return: HttpResponse
        """
        self.location_slug = kwargs['location_slug']
        return super(LocationFromRequestMixin, self).dispatch(request, *args, **kwargs)

    def get_location(self):
        """
        Gets the location based on the location_slug.
        """
        return get_object_or_404(self.location_queryset, slug=self.location_slug)

    def get_context_data(self, **kwargs):
        """
        Adds the location to the context.
        :type kwargs: {}
        :return: {}
        """
        context_data = super(LocationFromRequestMixin, self).get_context_data(**kwargs)
        context_data['location'] = self.get_location()
        return context_data
