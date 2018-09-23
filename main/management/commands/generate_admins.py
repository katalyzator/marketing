# coding=utf-8
from django.core.management import BaseCommand

from main.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(1, 8):
            user, flag = User.objects.get_or_create(username="newlife_" + str(i),
                                                    level=Products.objects.order_by('-level').first(),
                                                    email='newlife_' + str(i) + '@gmail.com',
                                                    phone='996550072079',
                                                    account='996550072079',
                                                    region=str(random.choice(string.digits)),
                                                    city=''.join(
                                                        random.choice(string.ascii_letters) for _ in range(10)))
            user.set_password('newlife123')
        self.stdout.write(self.style.SUCCESS("Users successfully created!"))
