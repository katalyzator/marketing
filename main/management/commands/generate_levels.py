# coding=utf-8
from django.core.management import BaseCommand

from main.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(1, 8):
            level, flag = Products.objects.get_or_create(title=str(i) + "тариф", price=i * 100)
        self.stdout.write(self.style.SUCCESS("Users successfully created!"))
