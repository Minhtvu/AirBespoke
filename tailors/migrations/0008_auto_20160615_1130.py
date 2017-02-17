# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tailors', '0007_tailor_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tailor',
            name='orders',
            field=models.ManyToManyField(blank=True, null=True, to='shop.OrderItem'),
        ),
    ]
