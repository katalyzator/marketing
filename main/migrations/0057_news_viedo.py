# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-12-21 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0056_auto_20181114_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='viedo',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Видео'),
        ),
    ]