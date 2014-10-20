# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('world', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('physical_description', models.CharField(max_length=500)),
                ('personality', models.CharField(max_length=500)),
                ('skills', models.CharField(max_length=500)),
                ('full_biography', models.TextField(null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CharacterProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slots', models.IntegerField(default=2)),
                ('user', models.OneToOneField(related_name=b'character_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='character',
            name='character_profile',
            field=models.ForeignKey(to='characters.CharacterProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='character',
            name='home_town',
            field=models.ForeignKey(to='world.Location'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='character',
            name='race',
            field=models.ForeignKey(to='world.Race'),
            preserve_default=True,
        ),
    ]
