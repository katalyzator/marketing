# coding=utf-8
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from jet.dashboard.modules import DashboardModule
from jet.utils import context_to_dict

from main.models import *


class BonusesQuantity(DashboardModule):
    """
    List of links widget.

    Usage example:

    .. code-block:: python

        from django.utils.translation import ugettext_lazy as _
        from jet.dashboard import modules
        from jet.dashboard.dashboard import Dashboard, AppIndexDashboard


        class CustomIndexDashboard(Dashboard):
            columns = 3

            def init_with_context(self, context):
                self.available_children.append(modules.LinkList)
                self.children.append(modules.LinkList(
                    _('Support'),
                    children=[
                        {
                            'title': _('Django documentation'),
                            'url': 'http://docs.djangoproject.com/',
                            'external': True,
                        },
                        {
                            'title': _('Django "django-users" mailing list'),
                            'url': 'http://groups.google.com/group/django-users',
                            'external': True,
                        },
                        {
                            'title': _('Django irc channel'),
                            'url': 'irc://irc.freenode.net/django',
                            'external': True,
                        },
                    ],
                    column=0,
                    order=0
                ))

    """

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
