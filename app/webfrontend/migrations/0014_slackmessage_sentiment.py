# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 10:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webfrontend', '0013_auto_20170207_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='slackmessage',
            name='sentiment',
            field=models.CharField(default=None, max_length=30, null=True),
        ),
    ]
