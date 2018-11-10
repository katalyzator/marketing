# coding=utf-8
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from jet.dashboard.modules import DashboardModule
from jet.utils import context_to_dict

from main.models import *


class BonusesQuantity(DashboardModule):
    title = _('Сумма бонусов')
    template = 'partials/bonus.html'
    # model =
    #: Specify widget layout.
    #: Allowed values ``stacked`` and ``inline``.
    layout = 'stacked'

    def get_context_data(self):
        context = context_to_dict(self.context)
        context.update({
            'module': self,
            'bonuses': User.objects.aggregate(sum=Sum('points'))['sum'],
            'buys': TransactionKeys.objects.aggregate(sum=Sum('product__price'))['sum'] / 2,
            'money': Payments.objects.aggregate(sum=Sum('sum'))['sum'] / 10
        })
        return context
