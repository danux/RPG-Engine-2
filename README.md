# RPG-Engine-2

Play-by-Post RPG for the modern web

[![Build Status](https://travis-ci.org/danux/RPG-Engine-2.svg?branch=master)](https://travis-ci.org/danux/RPG-Engine-2)


## Setup

Pretty standard Django 1.7 application.

```
git clone git@github.com:danux/RPG-Engine-2.git
pip install -r requirements.txt
```

Make a blank settings file in `soj/` and have it import the development settings.

This send email to the command line and some other useful stuff.

```
#  -*-coding: utf-8 -*-
"""
User specific settings.
"""
from soj.settings_development import *
```

You will need to use Celery to process sending email.

That means running a message broker and setting `settings.CELERY_BROKER`

```
./celery.sh
```

Then run the tests

```
python manage.py test
```
