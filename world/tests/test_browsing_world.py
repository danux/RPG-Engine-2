# -*- coding: utf-8 -*-
"""
Tests that continents and towns can be listed.
"""
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from rpg_auth.tests.utils import CreateUserMixin
from world.models import Continent, Location


class ListContinentsTestCase(CreateUserMixin):
    """
    Tests that continents can be listed.
    """
    fixtures = ['world-test-data.json']

    def test_can_list_continents(self):
        """
        Tests that a user can list the continents.
        """
        response = self.client.get(reverse('world:continent_list'))
        self.assertEquals(response.status_code, 200)
        self.assertTrue(issubclass(response.context['view'].__class__, ListView))
        self.assertEquals(list(response.context['object_list']), list(Continent.objects.all()))

    def test_can_view_continent(self):
        """
        Tests that a continent can be viewed.
        """
        continent = Continent.objects.get(pk=1)
        response = self.client.get(
            reverse('world:continent_detail', kwargs={'slug': continent.slug})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTrue(issubclass(response.context['view'].__class__, DetailView))
        self.assertEquals(response.context['object'], continent)


class DetailLocationTestCase(CreateUserMixin):
    """
    Tests that a location can be viewed.
    """
    fixtures = ['world-test-data.json']

    def test_can_view_location(self):
        """
        Tests that a location can be viewed.
        """
        location = Location.objects.get(pk=1)
        response = self.client.get(
            reverse('world:location_detail', kwargs={'slug': location.slug})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTrue(issubclass(response.context['view'].__class__, DetailView))
        self.assertEquals(response.context['object'], location)
