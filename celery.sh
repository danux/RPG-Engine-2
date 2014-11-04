#!/bin/bash
export DJANGO_SETTINGS_MODULE=soj.settings_ddavies
celery -A tasks worker --loglevel=info
