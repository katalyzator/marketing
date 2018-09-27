import random
import string

from django.core.management import BaseCommand
from next_prev import next_in_order

from main.models import TransactionKeys, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.all():
            user.wallet_id = None
            user.save()
            user.wallet_id = ''.join(random.choice(string.digits) for _ in range(7))
            user.save()
