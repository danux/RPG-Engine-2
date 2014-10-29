# -*- coding: utf-8 -*-
"""
Views related to questing.
"""
from braces.views import LoginRequiredMixin
from characters.mixins import CharacterFromRequestMixin, NoAvailableCharactersMixin
from characters.views import CharacterListView
from django.views.generic import CreateView, DetailView
from quests.forms import CreateQuestModelForm
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


class QuestCreateView(LoginRequiredMixin, NoAvailableCharactersMixin, CharacterFromRequestMixin,
                      LocationFromRequestMixin, CreateView):
    """
    Once a user has selected a location and a character they may create a quest.
    """
    model = Quest
    form_class = CreateQuestModelForm

    def __init__(self):
        super(QuestCreateView, self).__init__()
        self.object = None

    def get_character_queryset(self):
        """
        Limits the queryset to just the user's characters
        """
        return self.request.user.character_profile.available_characters

    def form_valid(self, form):
        """
        Adds the character and the location to the quest.
        :type form: CreateQuestModelForm
        :return: HttpResponse
        """
        self.object = form.save(commit=False)
        self.object.initialise(
            gm=self.request.user.quest_profile,
            first_post=form.cleaned_data['first_post'],
            location=self.get_location(),
            character=self.get_character(),
        )
        return super(QuestCreateView, self).form_valid(form)

    def get_success_url(self):
        """
        Redirects to the newly created quest.
        """
        return self.object.get_absolute_url()


class QuestDetailView(DetailView):
    """
    Details a quest
    """
    model = Quest
