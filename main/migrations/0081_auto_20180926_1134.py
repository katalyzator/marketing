# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-09-26 05:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0080_auto_20180925_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='wallet_id',
            field=models.CharField(default='4810084', max_length=8, unique=True, verbose_name='\u041b\u0438\u0446\u0435\u0432\u043e\u0439 \u0441\u0447\u0435\u0442'),
        ),
    ]
