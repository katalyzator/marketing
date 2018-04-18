# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import smart_unicode
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

levels = (
    ('1', 'Уровень 1'),
    ('2', 'Уровень 2'),
    ('3', 'Уровень 3'),
    ('4', 'Уровень 4'),
    ('5', 'Уровень 5'),
    ('6', 'Уровень 6'),
)


class TransactionKeys(models.Model):
    class Meta:
        verbose_name = 'Ключ'
        verbose_name_plural = 'Ключи синхронизации'

    handler = models.ForeignKey("User", verbose_name='Владелец ключа', related_name='handler')
    used_by = models.ForeignKey("User", verbose_name='Ипользовано', related_name='used_by')
    key = models.UUIDField(default=uuid.uuid4())

    def __unicode__(self):
        return smart_unicode(self.handler)


class Slider(models.Model):
    title = models.CharField(max_length=500, verbose_name='Заголовок')
    description = models.TextField(max_length=400, verbose_name='Описание')
    image = models.ImageField(upload_to='images/slider', verbose_name='Картинка')

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Раздел слайдов'

    def __unicode__(self):
        return smart_unicode(self.title)


class User(SimpleEmailConfirmationUserMixin, AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    level = models.CharField(verbose_name='Текущий уровень', choices=levels, max_length=255)
    email = models.EmailField(verbose_name='Email', unique=True)
    related_users = models.ManyToManyField("User", verbose_name='Рефералы')

    def __unicode__(self):
        if self.username:
            return smart_unicode(self.username)
        return smart_unicode(self.email)
