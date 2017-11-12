# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-11 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GamesList',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('game_date', models.DateField(blank=True, null=True)),
                ('away_team', models.CharField(blank=True, max_length=32, null=True)),
                ('away_team_score', models.IntegerField(blank=True, null=True)),
                ('home_team', models.CharField(blank=True, max_length=32, null=True)),
                ('home_team_score', models.IntegerField(blank=True, null=True)),
                ('game_id', models.CharField(blank=True, max_length=12, null=True)),
                ('overtime', models.CharField(blank=True, max_length=2, null=True)),
                ('attendance', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]