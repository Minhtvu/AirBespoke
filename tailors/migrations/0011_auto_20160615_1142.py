# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tailors', '0010_auto_20160615_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tailor',
            name='orders',
        ),
        migrations.AddField(
            model_name='tailor',
            name='orders',
            field=models.BooleanField(default=True),
        ),
    ]
