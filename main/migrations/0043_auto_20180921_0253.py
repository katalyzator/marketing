# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-09-20 20:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_auto_20180921_0247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='wallet_id',
            field=models.CharField(default=b'B9E9CCDC', max_length=8),
        ),
    ]
