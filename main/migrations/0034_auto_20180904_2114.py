# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-09-04 15:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_auto_20180904_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='wallet_id',
            field=models.CharField(default=b'F2249FEF', max_length=8),
        ),
        migrations.AlterField(
            model_name='video',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='main.Products', verbose_name='\u0423\u0440\u043e\u0432\u0435\u043d\u044c'),
        ),
    ]
