# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin

from main.models import *
from marketing import settings
from import_export.widgets import ForeignKeyWidget

# Register your models here.

admin.site.site_header = 'Панель управления'


class UserResource(resources.ModelResource):
    parent = fields.Field(attribute='get_parent')

    class Meta:
        model = User
        exclude = (
            'id',
            'last_login',
            'is_superuser',
            'groups',
            'user_permissions',
            'is_staff',
            'is_active',
            'date_joined',
            'level',
            'email',
            'related_users'
        )

    # def clean_parent(self, user):
    #     return user.get_parent


# def dehydrate_parent(self, user):
#
#     try:
#         return User.objects.get(related_users=user)
#     except:
#         return None
# if user and user.get_parent:
#     return user.get_parent
# return None


class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    search_fields = ['username', 'points', 'wallet_id', 'first_name', 'last_name', 'email', ]
    list_display = ['username', 'points', 'get_real_cash', 'level', 'first_name', 'wallet_id', 'email', 'is_active',
                    'level',
                    'date_joined']
    list_filter = ['level', 'is_active', ]

    # class Media:
    #     js = [
    #         'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js',
    #         settings.STATIC_URL + 'admin/js/export_to_excel.js'
    #     ]

    def get_real_cash(self, obj):
        payments = Payments.objects.filter(user=obj).aggregate(sum=Sum('sum', output_field=models.DecimalField()))[
                       'sum'] or decimal.Decimal(0)
        to_me_transfers = Transfer.objects.filter(to_user=obj).aggregate(
            sum=Sum('amount', output_field=models.DecimalField()))['sum'] or decimal.Decimal(0)
        my_transfers = Transfer.objects.filter(
            from_user=obj).aggregate(sum=Sum('amount', output_field=models.DecimalField()))['sum'] or decimal.Decimal(0)
        my_transactions = TransactionKeys.objects.filter(
            handler=obj).aggregate(
            sum=Sum('product__price', output_field=models.DecimalField()))['sum']
        to_me_transactions = TransactionKeys.objects.filter(used_by=obj).aggregate(
            sum=Sum('product__price', output_field=models.DecimalField()))['sum']
        if not my_transactions:
            my_transactions = 0
        to_me_transactions = to_me_transactions / 2 if to_me_transactions else 0
        payments = payments / 10 if payments else 0
        return payments + to_me_transfers + to_me_transactions - my_transfers - my_transactions

    def get_products(self, obj):
        return "\n".join([p.username for p in obj.related_users.all()])


class TransactionKeysAdmin(admin.ModelAdmin):
    list_display = ('handler', 'used_by', 'product', 'timestamp', 'updated')
    search_fields = ('handler', 'used_by',)


class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_bonus', 'timestamp', ]

    def get_bonus(self, obj):
        return obj.sum / 10

    get_bonus.short_description = 'Бонусы'


class CashRequestsAdmin(admin.ModelAdmin):
    list_display = ['points', 'user', 'user_account', 'timestamp', 'updated']

    def user_account(self, obj):
        return obj.user.account

    def get_queryset(self, request):
        return self.model.objects.filter(is_payed=False)


class TransferAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'amount', 'timestamp', 'updated']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp', 'updated']
    prepopulated_fields = {"slug": ("title",)}


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
