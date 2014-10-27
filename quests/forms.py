# -*- coding: utf-8 -*-
"""
Forms for interacting with quests.
"""
from django import forms
from quests.models import Quest


class CreateQuestModelForm(forms.ModelForm):
    """
    Form used to create a quest.
    """
    first_post = forms.CharField(widget=forms.widgets.Textarea)

    class Meta(object):
        """
        Meta properties
        """
        fields = ['title', 'description']
        model = Quest
