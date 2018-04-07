# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import smart_unicode


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


