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
            user.save()
        for i in range(1, 8):
            if i < 8:
                user = User.objects.get(username="newlife_" + str(i))
                user.related_users.add(User.objects.get(username='newlife_' + str(i + 1)))
                user.save()
        self.stdout.write(self.style.SUCCESS("Users successfully created!"))
