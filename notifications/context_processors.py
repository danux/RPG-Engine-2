# -*- coding: utf-8 -*-
"""
Adds unseen notifications to the context.
"""


def unseen_notifications(request):
    """
    Adds unseen notifications to the request.
    :param request: HttpRequest
    :return: {}
    """
    if request.user.is_authenticated():
        return {'unseen_notifications': request.user.notification_profile.unseen_notifications}
    else:
        return {'unseen_notifications': []}
