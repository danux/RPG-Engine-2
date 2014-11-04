#  -*-coding: utf-8 -*-
"""
User specific settings.
"""
from soj.settings import *


# Developers always push email to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# PEP-8
# INSTALLED_APPS += (
#     'test_pep8',
# )
PROJECT_DIR = os.path.dirname(__file__)
TEST_PEP8_DIRS = [os.path.dirname(PROJECT_DIR), ]
TEST_PEP8_EXCLUDE = ['migrations', ]
TEST_PEP8_IGNORE = ['E501', ]
