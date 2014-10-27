# -*- coding: utf-8 -*-
"""
Views related to questing.
"""
from braces.views import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from characters.views import CharacterListView
from world.models import Location
from world.views import ContinentListView


class SelectLocationListView(LoginRequiredMixin, ContinentListView):
    """
    Users ContinentListView to allow a user to select a location to quest in.
    """
    def get_template_names(self):
        """
        If the user has available characters provide a template to select a character
        otherwise show a different templates.

        :return: unicode
        """
        if self.request.user.character_profile.available_characters.count() < 1:
            return u'quests/no_characters_available.html'
        else:
            return u'quests/select_location.html'


class SelectCharacterListView(CharacterListView):
    """
    Allows a user to select a character for a quest.
    """
    location_queryset = Location.objects.all()

    def __init__(self):
        super(SelectCharacterListView, self).__init__()
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
        return super(SelectCharacterListView, self).dispatch(request, *args, **kwargs)

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
        context_data = super(SelectCharacterListView, self).get_context_data(**kwargs)
        context_data['location'] = self.get_location()
        return context_data

    def get_queryset(self):
        """
        Returns a queryset of the user's available characters.
        """
        return self.request.user.character_profile.available_characters

    def get_template_names(self):
        """
        If the user has available characters provide a template to select a character
        otherwise show a different templates.

        :return: unicode
        """
        if self.object_list.count() < 1:
            return u'quests/no_characters_available.html'
        else:
            return u'quests/select_character.html'
