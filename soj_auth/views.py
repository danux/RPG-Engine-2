# ~*~ coding: utf-8 ~*~
"""
Views for the auth app.
"""
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
from django.views.generic import CreateView

from soj_auth.forms import UserCreateForm


class UserCreateView(CreateView):
    """
    Registration form allowing users to create an account.
    """
    model = get_user_model()
    form_class = UserCreateForm
    success_url = lazy(reverse, str)('soj_auth:register-confirmation')
