import datetime

from django.core.management import BaseCommand

from main.models import TransactionKeys


class Command(BaseCommand):
    def handle(self, *args, **options):
        date = datetime.datetime.today() - datetime.timedelta(days=30)
        for i in TransactionKeys.objects.filter(timestamp__gte=date):
            i.used_by.update_balance(-i.product.price)
            # _log(i.used_by.username + '---' + str(i.product.price / 2))
