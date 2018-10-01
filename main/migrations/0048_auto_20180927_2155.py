# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-09-27 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0047_auto_20180921_1411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cashrequests',
            name='is_payed',
        ),
        migrations.RemoveField(
            model_name='video',
            name='caption',
        ),
        migrations.AddField(
            model_name='cashrequests',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='cashrequests',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
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
        migrations.AddField(
            model_name='video',
            name='keycode',
            field=models.CharField(max_length=5, null=True, verbose_name='\u041a\u043b\u044e\u0447\u0435\u0432\u043e\u0435 \u0441\u043b\u043e\u0432\u043e \u0438\u043b\u0438 \u0431\u0443\u043a\u0432\u0430'),
        ),
        migrations.AlterField(
            model_name='cashrequests',
            name='points',
            field=models.PositiveIntegerField(choices=[(1000, '1000'), (2000, '2000')], verbose_name='\u0411\u043e\u043d\u0443\u0441\u044b'),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='amount',
            field=models.PositiveIntegerField(verbose_name='\u0421\u043a\u043e\u043b\u044c\u043a\u043e'),
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
            name='region',
            field=models.CharField(max_length=255, null=True, verbose_name='\u041e\u0431\u043b\u0430\u0441\u0442\u044c'),
        ),
        migrations.AlterField(
            model_name='user',
            name='wallet_id',
            field=models.CharField(max_length=8, null=True, verbose_name='\u041b\u0438\u0446\u0435\u0432\u043e\u0439 \u0441\u0447\u0435\u0442'),
        ),
    ]