# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-09-08 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_auto_20180908_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actions',
            name='verification_code',
            field=models.CharField(default=b'1efd', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='wallet_id',
            field=models.CharField(default=b'11533AD8', max_length=8),
        ),
    ]
