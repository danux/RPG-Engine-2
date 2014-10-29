# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0002_auto_20141020_2128'),
        ('world', '0001_initial'),
        ('quests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('character', models.ForeignKey(related_name=b'posts', to='characters.Character')),
                ('location', models.ForeignKey(related_name=b'posts', to='world.Location')),
                ('quest', models.ForeignKey(related_name=b'posts', to='quests.Quest')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
