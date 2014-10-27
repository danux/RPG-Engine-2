# -*- coding: utf-8 -*-
"""
Mixins that can be used for classes that need some default character behaviour.
"""
from django.shortcuts import get_object_or_404
from characters.models import Character


class CharacterFromRequestMixin(object):
    """
    Loads the location specified by location_slug and adds it to the context.

    If the location is invalid then a 404 is raised.
    """
    character_queryset = Character.objects.all()

    def __init__(self):
        super(CharacterFromRequestMixin, self).__init__()
        self.character_pk = None

    def dispatch(self, request, *args, **kwargs):
        """
        Adds the location to self.
        :param request: HttpRequest
        :param args: []
        :param kwargs: {}
        :return: HttpResponse
        """
        self.character_pk = kwargs['character_pk']
        return super(CharacterFromRequestMixin, self).dispatch(request, *args, **kwargs)

    def get_character_queryset(self):
        """
        Gets the character queryset.
        """
        return self.character_queryset

    def get_character(self):
        """
        Gets the location based on the location_slug.
        """
        return get_object_or_404(self.get_character_queryset(), pk=self.character_pk)

    def get_context_data(self, **kwargs):
        """
        Adds the location to the context.
        :type kwargs: {}
        :return: {}
        """
        context_data = super(CharacterFromRequestMixin, self).get_context_data(**kwargs)
        context_data['character'] = self.get_character()
        return context_data