# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-09-13 11:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_auto_20180910_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='wallet_id',
            field=models.CharField(default=b'7D293CEC', max_length=8),
        ),
    ]
