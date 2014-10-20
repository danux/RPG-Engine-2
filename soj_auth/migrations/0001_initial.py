# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SojUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('pen_name', models.CharField(unique=True, max_length=30, db_index=True)),
                ('email', models.EmailField(unique=True, max_length=75, db_index=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
