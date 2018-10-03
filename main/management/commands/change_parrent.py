# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand

from main.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        # print(options)
        try:
            username = options['username']
            new_sponsor = User.objects.get(username='zaripa1983')
            user = User.objects.get(username=username)
            new_user = user.copy_itself(new_sponsor)
            # new_sponsor.related_users.add(new_user)
        except ObjectDoesNotExist:
            print('No!')
