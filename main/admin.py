# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from main.models import *
from marketing import settings

admin.site.site_header = 'Панель управления'


class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'points', 'get_real_cash', 'wallet_id', 'first_name', 'last_name', 'email', ]
    list_display = ['username', 'points', 'get_real_cash', 'first_name', 'wallet_id', 'email', 'is_active', 'level',
                    'date_joined']
    list_filter = ['is_active', ]

    class Media:
        js = [
            'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js',
            settings.STATIC_URL + 'admin/js/export_to_excel.js'
        ]

    def get_real_cash(self, obj):
        payments = Payments.objects.filter(user=obj).aggregate(sum=Sum('sum', output_field=models.DecimalField()))[
                       'sum'] or decimal.Decimal(0)
        to_me_transfers = Transfer.objects.filter(to_user=obj).aggregate(
            sum=Sum('amount', output_field=models.DecimalField()))['sum'] or decimal.Decimal(0)
        my_transfers = Transfer.objects.filter(
            from_user=obj).aggregate(sum=Sum('amount', output_field=models.DecimalField()))['sum'] or decimal.Decimal(0)
        transfers_count = Transfer.objects.filter(
            from_user=obj).count() or decimal.Decimal(0)
        my_transactions = TransactionKeys.objects.filter(
            handler=obj).aggregate(
            sum=Sum('product__price', output_field=models.DecimalField()))['sum']
        to_me_transactions = TransactionKeys.objects.filter(used_by=obj).aggregate(
            sum=Sum('product__price', output_field=models.DecimalField()))['sum']
        my_transactions = my_transactions / 2 if my_transactions else 0
        to_me_transactions = to_me_transactions / 2 if to_me_transactions else 0
        return payments + to_me_transfers + to_me_transactions - my_transfers - transfers_count - my_transactions

    def get_products(self, obj):
        return "\n".join([p.username for p in obj.related_users.all()])


class TransactionKeysAdmin(admin.ModelAdmin):
    list_display = ('handler', 'used_by', 'product', 'timestamp', 'updated')
    search_fields = ('handler', 'used_by',)


class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_bonus', 'timestamp', ]

    def get_bonus(self, obj):
        return obj.sum / 10

    get_bonus.short_description = 'Баллы'


class CashRequestsAdmin(admin.ModelAdmin):
    list_display = ['points', 'user', 'user_account', 'timestamp', 'updated']

    def user_account(self, obj):
        return obj.user.account


class TransferAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'amount', 'timestamp', 'updated']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp', 'updated']


admin.site.register(Agree)
admin.site.register(Payments, PaymentsAdmin)
admin.site.register(Slider)
admin.site.register(User, UserAdmin)
admin.site.register(Products)
admin.site.register(TransactionKeys, TransactionKeysAdmin)
admin.site.register(SocialLinks)
admin.site.register(Transfer, TransferAdmin)
admin.site.register(CashRequests, CashRequestsAdmin)
admin.site.register(Video)
admin.site.register(News, NewsAdmin)
