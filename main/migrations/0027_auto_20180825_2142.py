# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-08-25 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20180825_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='wallet_id',
            field=models.UUIDField(default=b'E0AF9F5F'),
        ),
    ]
