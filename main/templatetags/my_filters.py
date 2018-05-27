# coding=utf-8
import json

import requests
from django import template
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from main.models import *

register = template.Library()


@register.simple_tag
def get_refs_count(request, product):
    return TransactionKeys.objects.filter(used_by=request.user, is_confirmed_by_user=True, is_confirmed_by_admin=True,
                                          product=product).count()


@register.simple_tag
def has_transaction(user):
    try:
        transaction = TransactionKeys.objects.get(Q(is_confirmed_by_user=False) | Q(is_confirmed_by_admin=False),
                                                  handler=user)
        return transaction
    except:
        return False


@register.simple_tag
def need_to_activate(user):
    try:
        TransactionKeys.objects.get(handler=user, is_confirmed_by_user=True,
                                    is_confirmed_by_admin=False)
        return True
    except:
        return False


@register.simple_tag
def get_parent_user(user):
    for pos, obj in enumerate(user.get_all_parents):
        if obj.level.level > user.level.level and pos == user.level.level:
            return obj
        elif obj.level.level > user.level.level and pos > user.level.level:
            return obj


@register.simple_tag
def get_ref_by_line(user, refs=None, line=None):
    if not refs:
        refs = list()
    if not line:
        line = 1
    if user.related_users:
        for item in user.related_users.all():
            refs.append(item)
            if item.related_users:
                line += 1
                get_ref_by_line(item, refs, line)
        return refs
    else:
        return False


@register.simple_tag
def set_flag(flag):
    if flag == "true":
        return True
    return False


@register.simple_tag
def return_mobilnik_params(request, transaction):
    current_site = get_current_site(request)
    r = requests.post("http://" + current_site.domain + reverse('mobilnik'),
                      data={'transaction_id': transaction.pk})
    # json_ = json.loads(r.content.decode())
    return r.content
