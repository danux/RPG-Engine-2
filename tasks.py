# -*- coding: utf-8 -*-
"""
Celery tasks used to process non-time critical jobs.
"""
from celery import Celery
from django.core.mail import send_mail


app = Celery('tasks', broker='amqp://guest@localhost//')


@app.task
def queue_send_mail(subject, message, from_email, email, **kwargs):
    """
    Allows mail to be queued for sending and taken off the request.
    """
    send_mail(subject, message, from_email, email, **kwargs)
