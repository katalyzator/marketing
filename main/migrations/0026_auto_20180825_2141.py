# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-08-25 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_user_wallet_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='wallet_id',
            field=models.UUIDField(default=b'27fa69a8'),
        ),
    ]
