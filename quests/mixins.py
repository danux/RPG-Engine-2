# -*- coding: utf-8 -*-
"""
<<<<<<< HEAD
Mixins that can be used for classes that need some default quest objects behaviour.
=======
Mixins that can be used for classes that need some default quest behaviour.
>>>>>>> 48b41eb49ce1f5477e1e25b89af36d332dfb3a9f
"""
from django.shortcuts import get_object_or_404
from quests.models import Quest


class QuestFromRequestMixin(object):
    """
<<<<<<< HEAD
    Loads the quest specified by quest_slug and adds it to the context.

    If the quest is invalid then a 404 is raised.
=======
    Loads the location specified by quest_slug and adds it to the context.

    If the location is invalid then a 404 is raised.
>>>>>>> 48b41eb49ce1f5477e1e25b89af36d332dfb3a9f
    """
    quest_queryset = Quest.objects.all()

    def __init__(self):
        super(QuestFromRequestMixin, self).__init__()
        self.quest_slug = None

    def dispatch(self, request, *args, **kwargs):
        """
        Adds the quest to self.
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
