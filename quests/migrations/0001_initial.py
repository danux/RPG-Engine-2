# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('characters', '0001_initial'),
        ('world', '0001_initial'),
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
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Quest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestCharacter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_departed', models.DateTimeField(null=True, blank=True)),
                ('character', models.ForeignKey(to='characters.Character')),
                ('quest', models.ForeignKey(to='quests.Quest')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_departed', models.DateTimeField(null=True, blank=True)),
                ('location', models.ForeignKey(to='world.Location')),
                ('quest', models.ForeignKey(to='quests.Quest')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(related_name=b'quest_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='quest',
            name='characters',
            field=models.ManyToManyField(to='characters.Character', through='quests.QuestCharacter'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quest',
            name='gm',
            field=models.ForeignKey(to='quests.QuestProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quest',
            name='locations',
            field=models.ManyToManyField(to='world.Location', through='quests.QuestLocation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='quest',
            field=models.ForeignKey(related_name=b'posts', to='quests.Quest'),
            preserve_default=True,
        ),
    ]
