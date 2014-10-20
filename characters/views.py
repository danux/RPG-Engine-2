# ~*~ coding: utf-8 ~*~
"""
Views related to managing characters.
"""
from braces.views import LoginRequiredMixin

from django.core.urlresolvers import reverse
from django.http import Http404
from django.utils.functional import lazy
from django.views.generic import CreateView, ListView

from characters.models import Character


class CharacterListView(LoginRequiredMixin, ListView):
    """
    Lists a user's characters
    """

    def get_queryset(self):
        """
        Returns only the logged in user's characters.
        """
        return self.request.user.character_profile.character_set.all()


class CharacterCreateView(LoginRequiredMixin, CreateView):
    """
    Character creation form.
    """
    model = Character
    fields = ['name', 'home_town', 'race', 'physical_description', 'personality', 'skills', 'full_biography']
    success_url = lazy(reverse, str)('characters:dashboard')

    def __init__(self):
        super(CharacterCreateView, self).__init__()
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        """
        Checks the user is eligible to create new characters
        :type request: HttpRequest
        :type args: []
        :type kwargs: {}
        :return: HttpResponse
        """
        if request.user.is_authenticated() and not request.user.character_profile.has_free_slot:
            raise Http404()
        return super(CharacterCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid create the character and ensure it belongs to the correct user.
        :type form: CharacterCreateForm
        """
        self.object = form.save(commit=False)
        self.object.character_profile = self.request.user.character_profile
        self.object.save()
        return super(CharacterCreateView, self).form_valid(form)
