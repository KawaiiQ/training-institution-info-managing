# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-10 02:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20170109_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='time',
            field=models.IntegerField(default=0),
        ),
    ]
