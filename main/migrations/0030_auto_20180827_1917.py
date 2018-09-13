# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-08-27 13:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_auto_20180827_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='to_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL, verbose_name='\u041a\u043e\u043c\u0443'),
        ),
        migrations.AlterField(
            model_name='user',
            name='wallet_id',
            field=models.CharField(default=b'0DFC1769', max_length=8),
        ),
    ]