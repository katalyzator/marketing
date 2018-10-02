# -*- coding: utf-8 -*-
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
from django.db.models.fields.related import ManyToManyField

from main.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        print(options)
        try:
            username = options['username']
            new_sponsor = User.objects.get(username='zaripa1983')
            old_sponsor = User.objects.get(username='brilliant618')
            user = User.objects.get(username=username)
            old_sponsor.related_users.remove(user)
            old_sponsor.save()
            new_sponsor.related_users.add(user)
            self.copy_user(user, old_sponsor)
        except ObjectDoesNotExist:
            print('No!')

    def copy_user(self, user, parent_user):
        data = self.to_dict(user)
        data['username'] = data['username'] + '_new'
        data['email'] = data['email'].split('@')[0] + datetime.datetime.today().date() + '@gmail.com'
        data['phone'] = str(data['phone']) + datetime.datetime.today().date()
        data['level'] = user.level
        data['pk'] = User.objects.last().pk + 1
        new_user = User.objects.create(**data)
        parent_user.related_users.add(new_user)
        parent_user.save()
        for item in user.related_users.all():
            self.copy_user(item, user)

    def to_dict(self, instance):
        opts = instance._meta
        data = {}
        for f in opts.concrete_fields + opts.many_to_many:
            if isinstance(f, ManyToManyField):
                if instance.pk is None:
                    data[f.name] = []
                else:
                    data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
            else:
                data[f.name] = f.value_from_object(instance)
        return data
