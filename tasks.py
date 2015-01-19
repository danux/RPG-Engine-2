# -*- coding: utf-8 -*-
"""
Celery tasks used to process non-time critical jobs.
"""
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail


app = Celery('tasks', broker=settings.CELERY_BROKER)


@app.task
def queue_send_mail(subject, message, from_email, email, **kwargs):
    """
    Allows mail to be queued for sending and taken off the request.

    :type subject: unicode
    :type message: unicode
    :type from_email: unicode
    :type email: unicode
    :type kwargs: {}
    """
    send_mail(subject, message, from_email, email, **kwargs)
