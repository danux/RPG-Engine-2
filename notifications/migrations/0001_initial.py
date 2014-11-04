# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_seen', models.DateTimeField(db_index=True, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GenericNotification',
            fields=[
                ('notification_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='notifications.Notification')),
                ('text', models.TextField()),
            ],
            options={
            },
            bases=('notifications.notification',),
        ),
        migrations.CreateModel(
            name='NotificationProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(related_name='notification_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='notification',
            name='notification_profile',
            field=models.ForeignKey(related_name='notifications', to='notifications.NotificationProfile'),
            preserve_default=True,
        ),
    ]
