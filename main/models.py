# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import smart_unicode
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin
from colorfield.fields import ColorField
from django.db.models import *


class Products(models.Model):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    title = models.CharField(verbose_name='Название продукта', max_length=255)
    level = models.PositiveIntegerField(verbose_name='Уровень продукта', unique=True)
    price = models.PositiveIntegerField(verbose_name='Цена продукта')
    price1 = models.PositiveIntegerField(verbose_name='Цена продукции', default=150)
    image = models.ImageField(upload_to='images/product_images', blank=True, null=True)
    color = ColorField(default='#FF0000')

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
    product = models.ForeignKey("Products", verbose_name='За товар', null=True)
    key_for_user = models.CharField(verbose_name='ID транзакции для пользователя', null=True, unique=True,
                                    max_length=255)
    is_confirmed_by_user = models.BooleanField(verbose_name='Подтвержден пользователем', default=False)
    is_confirmed_by_admin = models.BooleanField(verbose_name='Подтвержден админом', default=False)

    def __unicode__(self):
        return smart_unicode(self.handler)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.is_confirmed_by_user and self.is_confirmed_by_admin:
            self.handler.level = self.product
        else:
            try:
                self.handler.level = Products.objects.get(level__lt=self.product.level)
            except:
                self.handler.level = None
        self.handler.save()
        super(TransactionKeys, self).save()

    @property
    def confirm_as_admin(self):
        self.is_confirmed_by_admin = True
        self.save()


class Slider(models.Model):
    title = models.CharField(max_length=500, verbose_name='Заголовок', null=True, blank=True)
    description = models.TextField(max_length=400, verbose_name='Описание', null=True, blank=True)
    image = models.ImageField(upload_to='images/slider', verbose_name='Картинка')

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Раздел слайдов'
        ordering = ['timestamp']

    def __unicode__(self):
        return str(self.title)


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

    @property
    def get_parent(self):
        return User.objects.filter(related_users=self).first()

    @property
    def get_all_parents(self):
        parents_array = []
        user = self
        for i in range(7):
            try:
                user = User.objects.get(level__gte=user, related_users=user)
                parents_array.append(user)
            except:
                user = User.objects.filter(related_users=user).first()
                parents_array.append(user)
        return parents_array

    @property
    def get_earned_money(self):
        if self.level:
            summ = TransactionKeys.objects.filter(used_by=self, is_confirmed_by_user=True,
                                                  is_confirmed_by_admin=True).aggregate(
                Sum('product__price')).get('product__price__sum')
            if summ:
                return summ
            else:
                return 0
        else:
            return 0


class SocialLinks(models.Model):
    class Meta:
        verbose_name_plural = 'Ссылки на соцсети'
        verbose_name = 'Ссылка'

    title = models.CharField(verbose_name='Название соцсети', max_length=255)
    link = models.URLField(verbose_name='Ссылка на соцсеть')
    icon = models.FileField(verbose_name='Иконка')
    icon_code = models.CharField(verbose_name='Код иконки',
                                 help_text='Код вы можете взять на сайте fontawesome.io/icons', max_length=255)

    def __unicode__(self):
        return smart_unicode(self.title)


class Agree(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    text = RichTextUploadingField(verbose_name='Контент')

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name_plural = 'Соглашение'
        verbose_name = 'соглашение'

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Agree, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
