# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ckeditor_uploader.fields import RichTextUploadingField
from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import smart_unicode
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin
import uuid

region_choices = (
    ('1', 'Чуй'),
    ('2', 'Ош'),
    ('3', 'Баткен'),
    ('4', 'Джалал-Абад'),
    ('5', 'Иссык-Куль'),
    ('6', 'Нарын'),
    ('6', 'Талас'),
)

cash_request_choices = ((1000, '1000'), (2000, '2000'))


class Products(models.Model):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    title = models.CharField(verbose_name='Название продукта', max_length=255)
    level = models.PositiveIntegerField(verbose_name='Уровень продукта', unique=True)
    price = models.PositiveIntegerField(verbose_name='Цена продукта с учетом для компании')
    # price1 = models.PositiveIntegerField(verbose_name='Цена продукции', default=150)
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

    # key_for_user = models.CharField(verbose_name='ID транзакции для пользователя', null=True, unique=True,
    #                                 max_length=255)
    # is_confirmed_by_user = models.BooleanField(verbose_name='Подтвержден пользователем', default=False)
    # is_confirmed_by_admin = models.BooleanField(verbose_name='Подтвержден админом', default=False)

    def __unicode__(self):
        return smart_unicode(self.handler)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        created = self.pk is None
        if created:
            self.handler.level = self.product
            self.handler.update_balance(-self.product.price / 2)
            self.used_by.update_balance(self.product.price / 2)
        super(TransactionKeys, self).save()

    @property
    def confirm_as_admin(self):
        self.is_confirmed_by_admin = True
        self.save()


class Transfer(models.Model):
    class Meta:
        verbose_name = 'Перевод баллов'
        verbose_name_plural = 'Переводы баллов'

    from_user = models.ForeignKey("User", related_name='from_user', verbose_name='От кого', on_delete=models.CASCADE,
                                  null=True)
    to_user = models.ForeignKey("User", related_name='to_user', verbose_name='Кому', on_delete=models.CASCADE,
                                null=True)
    amount = models.PositiveIntegerField(verbose_name='Сколько', default=0)

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.from_user)


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
    account = models.CharField(verbose_name='Расчетный счет', max_length=255, null=True)
    region = models.CharField(verbose_name='Область', choices=region_choices, max_length=255, null=True)
    city = models.CharField(verbose_name='Город', max_length=255, null=True)
    points = models.DecimalField(verbose_name='Баллы', default=0.0, max_digits=15, decimal_places=2, null=True)
    related_users = models.ManyToManyField("User", verbose_name='Рефералы', blank=True)
    wallet_id = models.CharField(max_length=8, default=uuid.uuid4().hex[:8].upper())

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
                if user:
                    parents_array.append(user)
                else:
                    break
            except:
                user = User.objects.filter(related_users=user).first()
                if user:
                    parents_array.append(user)
                else:
                    break
        return parents_array

    @property
    def get_earned_money(self):
        if self.level:
            summ = TransactionKeys.objects.filter(used_by=self).aggregate(
                Sum('product__price')).get('product__price__sum')
            if summ:
                return summ
            else:
                return 0
        else:
            return 0

    def update_balance(self, amount):
        self.points += amount
        return self.save()

    def is_validate(self):
        try:
            self.full_clean()
            return True
        except:
            return False


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


class Gallery(models.Model):
    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галерея'

    image = models.ImageField(verbose_name='Картинка', upload_to='gallery/')
    caption = models.CharField(verbose_name='Описание', max_length=255)

    def __str__(self):
        return str(self.caption)


class Video(models.Model):
    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    product = models.ForeignKey(Products, verbose_name='Уровень', on_delete=models.CASCADE, related_name='lessons',
                                null=True)
    video = models.FileField(verbose_name='Видео', upload_to='video/')
    caption = models.CharField(verbose_name='Описание', max_length=255)

    def __str__(self):
        return str(self.caption)


class Payments(models.Model):
    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    txn_id = models.CharField(verbose_name='Ключ транзакции', max_length=255, unique=True)
    date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')

    def __str__(self):
        return str(self.user)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        created = self.pk is None
        if created:
            self.user.update_balance(self.sum / 10)
        return super(Payments, self).save()


class CashRequests(models.Model):
    class Meta:
        verbose_name_plural = 'Запросы на обналичивание'
        verbose_name = 'Запрос на обналичивание'

    points = models.PositiveIntegerField(choices=cash_request_choices)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    is_payed = models.BooleanField(verbose_name='Деньги переведены')

    def __str__(self):
        return str(self.points)


@receiver(post_save, sender=Transfer, dispatch_uid="update_stock_count")
def transfer(sender, instance, created, **kwargs):
    if created:
        instance.from_user.update_balance(-instance.amount)
        instance.to_user.update_balance(instance.amount)


@receiver(post_save, sender=CashRequests, dispatch_uid="update_stock_count")
def update_balance(sender, instance, created, **kwargs):
    if not created and instance.is_payed:
        instance.user.update_balance(-int(float(instance.points)))
