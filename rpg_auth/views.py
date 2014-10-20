# -*- coding: utf-8 -*-
"""
Views for the auth app.
"""
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.forms import Form
from django.http import Http404
from django.utils.functional import lazy
from django.views.generic import CreateView, FormView

from rpg_auth.forms import UserCreateForm


class UserCreateView(CreateView):
    """
    Registration form allowing users to create an account.
    """
    model = get_user_model()
    form_class = UserCreateForm
    success_url = lazy(reverse, str)('rpg_auth:register_confirmation')

    def form_valid(self, form):
        """
        If the form is valid, generate and activation key and send the welcome email.

        :param form: The form that is valid
        :type form: UserCreateForm
        :return: HttpResponse
        """
        response = super(UserCreateView, self).form_valid(form)
        self.object.generate_activation_key()
        self.object.send_welcome_email(self.request)
        return response


class ActivateFormView(FormView):
    """
    Form used for activating accounts.
    """
    form_class = Form
    template_name = 'rpg_auth/activation_form.html'
    success_url = lazy(reverse, str)('rpg_auth:activation_confirmation')

    def __init__(self):
        super(ActivateFormView, self).__init__()
        self.activation_key = None
        self.user = None

    def dispatch(self, request, *args, **kwargs):
        """
        Loads the user by the activation key
        :type request: HttpRequest
        :type args: [] | ()
        :type kwargs: {}
        :return: HttpResponse
        """
        self.activation_key = kwargs['activation_key']
        if not self.load_user():
            raise Http404()
        return super(ActivateFormView, self).dispatch(request, *args, **kwargs)

    def load_user(self):
        """
        Loads the user based on the activation key.
        """
        try:
            self.user = get_user_model().objects.get_by_activation_key(activation_key=self.activation_key)
        except get_user_model().DoesNotExist:
            return False
        else:
            return True

    def form_valid(self, form):
        """
        If the form is valid (i.e. it has been posted to) then activate the user.
        :param form: Form
        """
        self.user.activate(self.request)
        self.user.save()
        return super(ActivateFormView, self).form_valid(form)
