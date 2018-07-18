# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.contrib import admin

# Register your models here.
from main.models import *
from marketing.settings import BASE_DIR

admin.site.site_header = 'Панель управления'


class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'first_name', 'last_name', 'email', ]
    list_display = ['username', 'first_name', 'email', 'is_active', 'level', 'date_joined']
    list_filter = ['is_active', ]

    def get_products(self, obj):
        return "\n".join([p.username for p in obj.related_users.all()])


class TransactionKeysAdmin(admin.ModelAdmin):
    list_display = ('handler', 'used_by', 'key_for_user')
    list_filter = ('handler', 'used_by', 'key_for_user')


admin.site.register(Agree)
admin.site.register(Slider)
admin.site.register(User, UserAdmin)
admin.site.register(Products)
admin.site.register(TransactionKeys, TransactionKeysAdmin)
admin.site.register(SocialLinks)
