# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-12 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_auto_20171212_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='barcode',
            field=models.BigIntegerField(blank=True, null=True, unique=True),
        ),
    ]