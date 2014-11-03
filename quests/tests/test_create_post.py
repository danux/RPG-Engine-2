# -*- coding: utf-8 -*-
"""
Tests creating posts on quests.
"""
from braces.views import LoginRequiredMixin
from django import forms
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from characters.tests.utils import CharacterUtils
from quests.models import Quest, Post
from rpg_auth.tests.utils import CreateUserMixin
from world.models import Location


class CreatePostTestCase(CreateUserMixin):
    """
    Tests that posts can be created.
    """
    fixtures = ['world-test-data.json']

    def setUp(self):
        super(CreatePostTestCase, self).setUp()
        self.character_1 = CharacterUtils.create_character(self.user)
        self.character_2 = CharacterUtils.create_character(self.user)
        self.location_1 = Location.objects.get(pk=1)
        self.quest = Quest(title=u'Quest')
        self.quest.initialise(
            gm=self.user.quest_profile, first_post=u'First post', character=self.character_1, location=self.location_1
        )
        self.user_1 = get_user_model().objects.create(email='test1@example.com', pen_name='Test 1')
        self.character_3 = CharacterUtils.create_character(self.user_1)
        self.quest.add_character(self.character_3)

    def test_can_render_post_view(self):
        """
        Tests that the view to post as post renders.
        """
        response = self.client.get(reverse('quests:create_post', kwargs={'quest_slug': self.quest.slug}))
        self.assertEquals(response.status_code, 200)
        self.assertTrue(issubclass(response.context['view'].__class__, CreateView))
        self.assertTrue(issubclass(response.context['view'].__class__, LoginRequiredMixin))
        form = response.context['form']
        self.assertEquals(len(form.fields), 2)
        self.assertIsInstance(form.fields['character'], forms.ModelChoiceField)
        self.assertIsInstance(form.fields['content'], forms.CharField)
        self.assertIsInstance(form.fields['content'].widget, forms.Textarea)

    def test_can_only_select_characters_on_quest(self):
        """
        Tests that the user can only select characters that belong to them and are on the quest.
        """
        response = self.client.get(reverse('quests:create_post', kwargs={'quest_slug': self.quest.slug}))
        character_field = response.context['form'].fields['character']
        self.assertTrue(self.character_1 in character_field.queryset)
        self.assertFalse(self.character_2 in character_field.queryset)
        self.assertFalse(self.character_3 in character_field.queryset)

    def test_submitting_post_sets_location(self):
        """
        When submitting a post the quest's current location should be the location
        of the post.
        """
        valid_data = {
            'character': self.character_1.pk,
            'content': u'Content',
        }
        response = self.client.post(
            reverse('quests:create_post', kwargs={'quest_slug': self.quest.slug}),
            data=valid_data,
            follow=True,
        )
        post = Post.objects.get(pk=2)
        self.assertRedirects(response, post.get_absolute_url())
        self.assertEquals(post.location, self.location_1)

    def test_if_user_does_not_have_character_on_quest_they_cannot_post(self):
        """
        If a user doesn't have a character on the quest they cannot post.
        """
        self.quest.remove_character(self.character_1)
        response = self.client.get(reverse('quests:create_post', kwargs={'quest_slug': self.quest.slug}))
        self.assertTemplateUsed(response, 'quests/no_characters_on_quest.html')
