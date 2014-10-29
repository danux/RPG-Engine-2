# -*- coding: utf-8 -*-
"""
Forms for interacting with quests.
"""
from django import forms
from quests.models import Quest, Post


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


class CreatePostModelForm(forms.ModelForm):
    """
    Form used for creating posts.
    """
    class Meta(object):
        """
        Meta properties
        """
        fields = ['character', 'content']
        model = Post
