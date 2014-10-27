# -*- coding: utf-8 -*-
"""
Mixins that can be used for classes that need some default quest objects behaviour.
"""


class NoAvailableCharactersMixin(object):
    """
    Mixin that checks if a user has available characters and renders to a special
    template if they don't.
    """
    def get_template_names(self):
        """
        If the user has available characters provide a template to select a character
        otherwise show a different templates.

        :return: unicode
        """
        if self.request.user.character_profile.has_available_characters:
            return super(NoAvailableCharactersMixin, self).get_template_names()
        else:
            return u'quests/no_characters_available.html'