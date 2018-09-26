# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-09-26 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0082_auto_20180926_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='payments',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='transactionkeys',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='transactionkeys',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='wallet_id',
            field=models.CharField(default='3000909', max_length=8, unique=True, verbose_name='\u041b\u0438\u0446\u0435\u0432\u043e\u0439 \u0441\u0447\u0435\u0442'),
        ),
    ]