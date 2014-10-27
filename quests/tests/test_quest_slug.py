# -*- coding: utf-8 -*-
"""
Tests that quests create slug properly.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from quests.models import Quest


class SlugTestCase(TestCase):
    """
    Tests that slugs are generated correctly for quests.
    """
    def test_slugify_occurs(self):
        """
        Tests basic slugify.
        """
        quest = Quest.objects.create(
            title=u'Test Quest',
            gm=get_user_model().objects.create(pen_name='test', email='test@example.com'),
        )
        self.assertEquals(quest.slug, 'test-quest')

    def test_slugify_fixes_clashes(self):
        """
        Tests that if slugs clash a hyphen is prepended.
        """
        Quest.objects.create(
            title=u'Test Quest',
            gm=get_user_model().objects.create(pen_name='test', email='test1@example.com'),
        )
        quest = Quest.objects.create(
            title=u'Test  Quest',
            gm=get_user_model().objects.create(pen_name='test2', email='test2@example.com'),
        )
        self.assertEquals(quest.slug, '-test-quest')
