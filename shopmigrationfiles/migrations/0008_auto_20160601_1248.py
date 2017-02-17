# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-01 18:48
from __future__ import unicode_literals

import cartridge.shop.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20150921_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='special',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=100, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='productvariation',
            name='option3',
            field=cartridge.shop.fields.OptionField(max_length=50, null=True, verbose_name='Tailor'),
        ),
        migrations.AlterField(
            model_name='productoption',
            name='type',
            field=models.IntegerField(choices=[(1, 'Size'), (2, 'Colour'), (3, 'Tailor')], verbose_name='Type'),
        ),
    ]