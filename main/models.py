# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string
import decimal
from ckeditor_uploader.fields import RichTextUploadingField
from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

region_choices = (
    ('1', 'Чуй'),
    ('2', 'Ош'),
    ('3', 'Баткен'),
    ('4', 'Джалал-Абад'),
    ('5', 'Иссык-Куль'),
    ('6', 'Нарын'),
    ('7', 'Талас'),
)

cash_request_choices = (
    (300, '300'),
    (500, '500'),
    (700, '700'),
    (2000, '2000'),
    (1000, '1000'),
    (2000, '2000'),
)


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

    def __str__(self):
        return str(self.title)

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

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

    def __str__(self):
        return str(self.handler)


class Transfer(models.Model):
    class Meta:
        verbose_name = 'Перевод баллов'
        verbose_name_plural = 'Переводы баллов'

    from_user = models.ForeignKey("User", related_name='from_user', verbose_name='От кого', on_delete=models.CASCADE,
                                  null=True)
    to_user = models.ForeignKey("User", related_name='to_user', verbose_name='Кому', on_delete=models.CASCADE,
                                null=True)
    amount = models.PositiveIntegerField(verbose_name='Сколько')

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

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

    def __str__(self):
        return str(self.title)


class User(SimpleEmailConfirmationUserMixin, AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    level = models.ForeignKey(Products, verbose_name='Текущий уровень', on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(verbose_name='Email', unique=True)
    phone = models.CharField(verbose_name='Номер телефона', max_length=255, null=True)
    account = models.CharField(verbose_name='Расчетный счет', max_length=255, null=True)
    country = models.CharField(verbose_name='Страна', null=True, max_length=255)
    region = models.CharField(verbose_name='Область', max_length=255, null=True)
    city = models.CharField(verbose_name='Город', max_length=255, null=True)
    points = models.DecimalField(verbose_name='Баллы', default=0.0, max_digits=15, decimal_places=2, null=True)

    passport_id = models.CharField(verbose_name='Паспорт серии', null=True, max_length=255)
    INN = models.CharField(verbose_name='ИНН', max_length=255, null=True)
    district = models.CharField(verbose_name='Район', null=True, max_length=255)
    address = models.CharField(verbose_name='Адрес', null=True, max_length=255)
    related_users = models.ManyToManyField("User", verbose_name='Рефералы', blank=True)
    wallet_id = models.CharField(max_length=8, verbose_name='Лицевой счет', null=True)

    def __str__(self):
        if self.username:
            return str(self.username)
        return str(self.email)

    def save(self, *args, **kwargs):
        if not self.wallet_id:
            try:
                user = User.objects.get(wallet_id=self.wallet_id)
                if not user == self:
                    self.wallet_id = ''.join(random.choice(string.digits) for _ in range(7))
                    self.save(*args, **kwargs)
                else:
                    super(User, self).save(*args, **kwargs)
            except ObjectDoesNotExist:
                self.wallet_id = ''.join(random.choice(string.digits) for _ in range(7))
                self.save(*args, **kwargs)
        super(User, self).save(*args, **kwargs)

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

    def copy_itself(self, parent_user):
        related_users = self.related_users.all()
        user = self
        user.phone = user.phone.replace(user.phone[-1], '3', 1)
        user.save()
        user.pk = User.objects.last().pk + 1
        user.username = user.username + '3'
        user.email = user.email.split('@')[0] + '_3' + user.email.split('@')[1]
        user.wallet_id = None
        user.phone.replace(user.phone[-1], '', 1)
        user.save()
        new_user = user
        new_user.related_users.clear()
        new_user.save()
        parent_user.related_users.add(new_user)
        parent_user.save()
        if related_users:
            for i in related_users.all():
                i.copy_itself(new_user)
        return new_user

    @property
    def get_earned_money(self):
        if self.level:
            summ = TransactionKeys.objects.filter(used_by=self).aggregate(
                Sum('product__price')).get('product__price__sum')
            if summ:
                return summ / 2
            else:
                return 0
        else:
            return 0

    def update_balance(self, amount):
        self.points += decimal.Decimal(amount)
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

    def __str__(self):
        return str(self.title)


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
    keycode = models.CharField(verbose_name='Ключевое слово или буква', max_length=5, null=True)

    def __str__(self):
        return str(self.keycode)


class Payments(models.Model):
    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    txn_id = models.CharField(verbose_name='Ключ транзакции', max_length=255, unique=True)
    date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

    def __str__(self):
        return str(self.user)


class CashRequests(models.Model):
    class Meta:
        verbose_name_plural = 'Запросы на обналичивание'
        verbose_name = 'Запрос на обналичивание'

    points = models.PositiveIntegerField(verbose_name='Бонусы', choices=cash_request_choices)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    # is_payed = models.BooleanField(verbose_name='Деньги переведены')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

    def __str__(self):
        return str(self.points)


class News(models.Model):
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    title = models.CharField(verbose_name='Название новости', max_length=255)
    preview = models.ImageField(verbose_name='Картинка новости', null=True)
    text = RichTextUploadingField(verbose_name='Содержимое новости', null=True)
    slug = models.SlugField(verbose_name='Слаг', unique=True, default='')

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

    def __str__(self):
        return str(self.title)


@receiver(post_save, sender=Transfer, dispatch_uid="update_stock_count")
def transfer(sender, instance, created, **kwargs):
    if created:
        instance.from_user.update_balance(-instance.amount)
        instance.to_user.update_balance(instance.amount - 1)


@receiver(post_save, sender=CashRequests, dispatch_uid="update_stock_count")
def update_balance(sender, instance, created, **kwargs):
    if created:
        instance.user.update_balance(-int(float(instance.points)))


@receiver(post_save, sender=Payments, dispatch_uid="update_stock_count")
def update_balance(sender, instance, created, **kwargs):
    if created:
        instance.user.update_balance((instance.sum) / decimal.Decimal(10))


@receiver(post_save, sender=TransactionKeys, dispatch_uid="sell_levels")
def set_level(sender, instance, created, **kwargs):
    if created:
        instance.handler.level = instance.product
        instance.handler.update_balance(-instance.product.price)
        instance.used_by.update_balance(instance.product.price / 2)
