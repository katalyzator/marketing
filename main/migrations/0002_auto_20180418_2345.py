# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-18 17:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionkeys',
            name='key',
            field=models.UUIDField(default=uuid.UUID('171519a8-63da-4f1f-a9f7-5f3fe0e49791')),
        ),
        migrations.RemoveField(
            model_name='user',
            name='related_users',
        ),
        migrations.AddField(
            model_name='user',
            name='related_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='\u0420\u0435\u0444\u0435\u0440\u0430\u043b\u044b'),
        ),
    ]
