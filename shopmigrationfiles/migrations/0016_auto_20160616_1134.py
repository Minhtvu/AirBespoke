# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-16 17:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_auto_20160616_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='fabrics',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fabrics.Fabric'),
        ),
        migrations.AlterField(
            model_name='product',
            name='fabrics',
            field=models.ManyToManyField(null=True, to='fabrics.Fabric'),
        ),
    ]