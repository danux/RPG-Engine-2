# ~*~ coding: utf-8 ~*~
"""
Views related to managing characters.
"""
from django.views.generic import CreateView

from characters.models import Character


class CharacterCreateView(CreateView):
    """
    Character creation form.
    """
    model = Character
