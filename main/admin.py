# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from main.models import *

admin.site.site_header = 'Панель управления'


class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'first_name', 'last_name', 'email', ]
    list_display = ['username', 'get_products' ,'first_name', 'last_name', 'email', 'is_active']
    list_filter = ['is_active', ]

    def get_products(self, obj):
        return "\n".join([p.username for p in obj.related_users.all()])

admin.site.register(Agree)
admin.site.register(Slider)
admin.site.register(User, UserAdmin)
admin.site.register(Products)
admin.site.register(TransactionKeys)
admin.site.register(SocialLinks)
