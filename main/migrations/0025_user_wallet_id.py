# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-08-25 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20180825_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='wallet_id',
            field=models.UUIDField(default=b'68bd2f5f76a341f18bdc31e1e8aba601'),
        ),
    ]
