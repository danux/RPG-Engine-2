# -*- coding: utf-8 -*-
"""
Authentication models.
"""
from __future__ import unicode_literals
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.sites.shortcuts import get_current_site
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext as _
from tasks import queue_send_mail


class RpgUserManager(BaseUserManager):
    """
    Custom manager for the SoJ User.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError(_('The given email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """
        Creates a user.

        :type email: unicode
        :type password: unicode
        :type extra_fields: {}
        """
        return self._create_user(email, password, **extra_fields)

    def get_by_activation_key(self, activation_key):
        """
        Gets a user by their activation key.

        :type activation_key: unicode
        """
        return self.get(activation_key=activation_key, is_active=False)

    def create_superuser(self, **kwargs):
        """
        Creates a superuser.
        :type kwargs: {}
        :rtype: RpgUser
        """
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(**kwargs)


class RpgUser(AbstractBaseUser):
    """
    The user class.
    """

    pen_name = models.CharField(unique=True, db_index=True, max_length=30)
    email = models.EmailField(unique=True, db_index=True)
    is_active = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=60)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = RpgUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['pen_name']

    def generate_activation_key(self):
        """
        Sets the activation_key to be a UUID.
        """
        self.activation_key = uuid.uuid1()

    def email_user(self, request, subject, template, context, from_email=None, **kwargs):
        """
        Sends an email to this User.

        :param subject: The subject of the email
        :param request: The request, used to get the domain
        :type request: HttpRequest
        :type subject: unicode
        :param template: The template to render the email message with
        :type template: unicode
        :param context: The context that should be used when rendering the template
        :type context: {}
        :param from_email: The email address the email should be from
        :type from_email: unicode
        :type kwargs: {}
        """
        current_site = get_current_site(request)
        context['domain'] = current_site.domain
        context['protocol'] = 'https' if request.is_secure() else 'http',

        message = render_to_string(template, context)
        queue_send_mail.delay(subject, message, from_email, [self.email], **kwargs)

    def send_welcome_email(self, request):
        """
        Sends the welcome email and activation key to the user.

        :type request: HttpRequest
        """
        context = {
            'user': self,
        }
        self.email_user(request, _('Welcome to SoJ!'), 'rpg_auth/email/activation_email.txt', context)

    def activate(self, request):
        """
        Activates a user's account

        :type request: HttpRequest
        """
        self.is_active = True
        context = {
            'user': self,
        }
        self.email_user(
            request,
            _('Your account has been activated!'),
            'rpg_auth/email/account_activated_email.txt',
            context,
        )
