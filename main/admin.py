# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from main.models import Slider

admin.site.site_header = 'Панель управления'


class SliderAdmin(admin.ModelAdmin):
    class Meta:
        model = Slider


admin.site.register(Slider, SliderAdmin)
