# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import smart_unicode
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin


class Products(models.Model):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    title = models.CharField(verbose_name='Название продукта', max_length=255)
    level = models.PositiveIntegerField(verbose_name='Уровень продукта', unique=True)
    price = models.PositiveIntegerField(verbose_name='Цена продукта')

    def __unicode__(self):
        return smart_unicode(self.title)

    @property
    def get_highest_product(self):
        product = Products.objects.order_by('level').filter(level__gt=self.level).first()
        return product


class TransactionKeys(models.Model):
    class Meta:
        verbose_name = 'Ключ'
        verbose_name_plural = 'Ключи синхронизации'

    handler = models.ForeignKey("User", verbose_name='Владелец ключа', related_name='handler')
    used_by = models.ForeignKey("User", verbose_name='Ипользовано', related_name='used_by')
    key = models.CharField(verbose_name='ID транзакции', null=True, max_length=255)
    is_confirmed = models.BooleanField(verbose_name='Подтвержден', default=False)

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

    level = models.ForeignKey(Products, verbose_name='Текущий уровень', on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(verbose_name='Email', unique=True)
    phone = models.CharField(verbose_name='Номер телефона', max_length=255, null=True)
    mobilnik = models.CharField(verbose_name='Мобильник кошелек', max_length=255, null=True)
    related_users = models.ManyToManyField("User", verbose_name='Рефералы', blank=True)

    def __unicode__(self):
        if self.username:
            return smart_unicode(self.username)
        return smart_unicode(self.email)
