# -*- coding: utf-8 -*-
"""
Mixins that can be used for classes that need some default quest behaviour.
"""
from django.shortcuts import get_object_or_404
from quests.models import Quest


class QuestFromRequestMixin(object):
    """
    Loads the location specified by quest_slug and adds it to the context.

    If the location is invalid then a 404 is raised.
    """
    quest_queryset = Quest.objects.all()

    def __init__(self):
        super(QuestFromRequestMixin, self).__init__()
        self.quest_slug = None

    def dispatch(self, request, *args, **kwargs):
        """
        Adds the location to self.
        :param request: HttpRequest
        :param args: []
        :param kwargs: {}
        :return: HttpResponse
        """
        self.quest_slug = kwargs['quest_slug']
        return super(QuestFromRequestMixin, self).dispatch(request, *args, **kwargs)

    def get_quest_queryset(self):
        """
        Gets the character queryset.
        """
        return self.quest_queryset

    def get_quest(self):
        """
        Gets the location based on the location_slug.
        """
        return get_object_or_404(self.get_quest_queryset(), slug=self.quest_slug)

    def get_context_data(self, **kwargs):
        """
        Adds the location to the context.
        :type kwargs: {}
        :return: {}
        """
        context_data = super(QuestFromRequestMixin, self).get_context_data(**kwargs)
        context_data['quest'] = self.get_quest()
        return context_data
