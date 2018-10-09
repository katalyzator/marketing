# coding=utf-8
from django.utils.translation import ugettext_lazy as _
from jet.dashboard.dashboard import Dashboard

from .modules import *
from jet.dashboard.modules import *


class CustomDashboard(Dashboard):
    columns = 4

    def init_with_context(self, context):
        # pass
        self.available_children.append(BonusesQuantity(_(u'Сумма бонусов'), ))
        self.children.append(BonusesQuantity(_(u'Сумма бонусов'), ))
