# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-08-27 10:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_auto_20180825_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='wallet_id',
            field=models.CharField(default=b'27ACB1EA', max_length=8),
        ),
    ]
