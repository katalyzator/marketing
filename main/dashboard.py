# coding=utf-8
from jet.dashboard.modules import DashboardModule


class BonusesCount(DashboardModule):
    title = 'Бонусов в обороте'
    title_url = ''
    template = 'partials/bonus.html'
    limit = 10
