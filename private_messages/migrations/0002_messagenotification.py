# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
        ('private_messages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageNotification',
            fields=[
                ('notification_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='notifications.Notification')),
                ('private_message', models.ForeignKey(to='private_messages.PrivateMessage')),
            ],
            options={
            },
            bases=('notifications.notification',),
        ),
    ]
