# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tailors', '0012_remove_tailor_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='tailor',
            name='test',
            field=models.BooleanField(default=True),
        ),
    ]
