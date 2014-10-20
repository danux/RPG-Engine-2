# ~*~ coding: utf-8 ~*~
"""
Authentication models.
"""
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class SojUser(AbstractBaseUser):
    """
    The user class.
    """
    pen_name = models.CharField(unique=True, db_index=True, max_length=30)
    email = models.EmailField(unique=True, db_index=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
