# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webfrontend', '0014_slackmessage_sentiment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slackmessage',
            name='ts',
            field=models.DateTimeField(db_index=True),
        ),
    ]
