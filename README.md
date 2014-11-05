# RPG-Engine-2

Play-by-Post RPG for the modern web

Master: [![Build Status](https://travis-ci.org/danux/RPG-Engine-2.svg?branch=master)](https://travis-ci
.org/danux/RPG-Engine-2)
Notifications: [![Build Status](https://travis-ci.org/danux/RPG-Engine-2.svg?branch=notifiations)](https://travis-ci.org/danux/RPG-Engine-2)


## Setup

Pretty standard Django 1.7 application.

```
git clone https://github.com/danux/RPG-Engine-2.git
pip install -r requirements.txt
```

Make a blank settings file in `soj/` and have it import the development settings.

This sends email to the command line, sets `DEBUG` and some other useful stuff.

```
#  -*-coding: utf-8 -*-
"""
User specific settings.
"""
from soj.settings_development import *
```

Then run the tests

```
python manage.py test --settings=soj.{your-settings-module>}
```

### Celery

You will need to use Celery to process sending email.

That means running a message broker and setting `settings.CELERY_BROKER`.

```
./celery.sh
```

## Status Message Views

Views that have confirmation messages to users.

### Characters

- Create character
- Follow character
- Unfollow character

### Quests

- Create quest
- Create post
- Join quest
- Leave quest
- Follow quest
- Unfollow quest
- Close quest

### Private Messages

- User blocked from sending private message


## Followable Content

Anything that can be followed, and therefore may have an influence on a timeline.

- Quests (QuestProfile)
- Characters (CharacterProfile)
