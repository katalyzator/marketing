# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-10-02 17:17
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0049_auto_20181001_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043d\u043e\u0432\u043e\u0441\u0442\u0438')),
                ('preview', models.ImageField(null=True, upload_to=b'', verbose_name='\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0430 \u043d\u043e\u0432\u043e\u0441\u0442\u0438')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='\u0421\u043e\u0434\u0435\u0440\u0436\u0438\u043c\u043e\u0435 \u043d\u043e\u0432\u043e\u0441\u0442\u0438')),
                ('slug', models.SlugField(default='', unique=True, verbose_name='\u0421\u043b\u0430\u0433')),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': '\u041d\u043e\u0432\u043e\u0441\u0442\u044c',
                'verbose_name_plural': '\u041d\u043e\u0432\u043e\u0441\u0442\u0438',
            },
        ),
    ]