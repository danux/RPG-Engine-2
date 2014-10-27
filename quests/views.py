# -*- coding: utf-8 -*-
"""
Views related to questing.
"""
from braces.views import LoginRequiredMixin
from django.views.generic import CreateView

from characters.mixins import CharacterFromRequestMixin
from characters.views import CharacterListView
from quests.forms import CreateQuestModelForm
from quests.mixins import NoAvailableCharactersMixin
from quests.models import Quest
from world.mixins import LocationFromRequestMixin
from world.views import ContinentListView


class SelectLocationListView(LoginRequiredMixin, NoAvailableCharactersMixin, ContinentListView):
    """
    Users ContinentListView to allow a user to select a location to quest in.
    """
    template_name = u'quests/select_location.html'


class SelectCharacterListView(NoAvailableCharactersMixin, LocationFromRequestMixin, CharacterListView):
    """
    Allows a user to select a character for a quest.
    """
    template_name = u'quests/select_character.html'

    def get_queryset(self):
        """
        Returns a queryset of the user's available characters.
        """
        return self.request.user.character_profile.available_characters


class QuestCreateView(NoAvailableCharactersMixin, CharacterFromRequestMixin, LocationFromRequestMixin, CreateView):
    """
    Once a user has selected a location and a character they may create a quest.
    """
    model = Quest
    form_class = CreateQuestModelForm

    def get_character_queryset(self):
        """
        Limits the queryset to just the user's characters
        """
        return self.request.user.character_profile.available_characters
