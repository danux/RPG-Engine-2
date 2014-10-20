# -*- coding: utf-8 -*-
"""
Views for the world.
"""
from django.views.generic import DetailView, ListView
from world.models import Continent, Location


class ContinentListView(ListView):
    """
    Lists the continents.
    """
    model = Continent


class ContinentDetailView(DetailView):
    """
    Details a continent.
    """
    model = Continent


class LocationDetailView(DetailView):
    """
    Details a location.
    """
    model = Location
