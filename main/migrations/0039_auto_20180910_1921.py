# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-09-10 13:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_auto_20180908_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashRequests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.PositiveIntegerField(choices=[(1000, '1000'), (2000, '2000')])),
                ('is_payed', models.BooleanField(verbose_name='\u0414\u0435\u043d\u044c\u0433\u0438 \u043f\u0435\u0440\u0435\u0432\u0435\u0434\u0435\u043d\u044b')),
            ],
            options={
                'verbose_name': '\u0417\u0430\u043f\u0440\u043e\u0441 \u043d\u0430 \u043e\u0431\u043d\u0430\u043b\u0438\u0447\u0438\u0432\u0430\u043d\u0438\u0435',
                'verbose_name_plural': '\u0417\u0430\u043f\u0440\u043e\u0441\u044b \u043d\u0430 \u043e\u0431\u043d\u0430\u043b\u0438\u0447\u0438\u0432\u0430\u043d\u0438\u0435',
            },
        ),
        migrations.RemoveField(
            model_name='actions',
            name='user',
        ),
        migrations.AlterField(
            model_name='user',
            name='wallet_id',
            field=models.CharField(default=b'2D938EFF', max_length=8),
        ),
        migrations.DeleteModel(
            name='Actions',
        ),
        migrations.AddField(
            model_name='cashrequests',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c'),
        ),
    ]