#!/bin/bash
export DJANGO_SETTINGS_MODULE=soj.settings_development
celery -A tasks worker --loglevel=info
