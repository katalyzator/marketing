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
def get_ref_by_line(parents_ids, level, curr_level=1):
    child_ids = []
    if type(parents_ids) == int:
        parents_ids = [parents_ids]
    for i in User.objects.filter(pk__in=parents_ids):
        for j in i.related_users.all():
            child_ids.append(j.pk)
    if curr_level == level:
        return User.objects.filter(pk__in=child_ids)
    curr_level += 1
    parents_ids = child_ids
    return get_ref_by_line(parents_ids, level, curr_level)


@register.simple_tag
def set_flag(flag):
    if flag == "true":
        return True
    return False
