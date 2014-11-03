# -*- coding: utf-8 -*-
from braces.views import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from characters.mixins import NoAvailableCharactersMixin, CharacterFromRequestMixin
from characters.views import CharacterListView
from quests.forms import CreateQuestModelForm, CreatePostModelForm
from quests.mixins import QuestFromRequestMixin
from quests.models import Quest, Post
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


class PostCreateView(LoginRequiredMixin, QuestFromRequestMixin, CreateView):
    """
    View that allows users to post to quests.
    """
    model = Post
    form_class = CreatePostModelForm

    def __init__(self):
        super(PostCreateView, self).__init__()
        self.object = None

    def get_template_names(self):
        """
        Returns an alternative template if the user has no character on the quest.
        """
        if self.get_quest().current_characters.filter_by_character_profile(
            character_profile=self.request.user.character_profile
        ).count() > 0:
            return super(PostCreateView, self).get_template_names()
        else:
            return 'quests/no_characters_on_quest.html'

    def get_form(self, form_class):
        """
        Limits the choices the character field to just characters that this user has.

        :type form_class: CreatePostModelForm
        """
        form = super(PostCreateView, self).get_form(form_class)
        form.fields['character'].queryset = self.get_quest().current_characters.filter_by_character_profile(
            character_profile=self.request.user.character_profile
        )
        return form

    def form_valid(self, form):
        """
        Sets the location and the quest for the post
        :type form: CreatePostModelForm
        """
        self.object = form.save(commit=False)
        self.object.location = self.get_quest().current_location
        self.object.quest = self.get_quest()
        self.object.save()
        return super(PostCreateView, self).form_valid(form)
