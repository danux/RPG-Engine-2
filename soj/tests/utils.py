# -*- coding: utf-8 -*-
"""
Utils for testing in all apps.
"""
from django.contrib.auth.models import AnonymousUser


class MockRequest(object):
    """
    Mock request with valid is_secure method.
    """
    def __init__(self):
        super(MockRequest, self).__init__()
        self.user = AnonymousUser()

    @staticmethod
    def is_secure():
        """
        Returns true.
        """
        return True

    @staticmethod
    def get_host():
        """
        Returns true.
        """
        return 'host'
