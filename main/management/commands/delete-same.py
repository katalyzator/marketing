from django.core.management import BaseCommand
from next_prev import next_in_order

from main.models import TransactionKeys


class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in TransactionKeys.objects.all():
            if not item == TransactionKeys.objects.last() and item.key_for_user == next_in_order(item,
                                                                                                 TransactionKeys.objects.all()).key_for_user:
                item.delete()
        print("Success!")
