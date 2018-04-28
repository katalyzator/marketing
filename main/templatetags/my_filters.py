from django import template

from main.models import *

register = template.Library()


@register.simple_tag
def get_refs_count(request, product):
    return TransactionKeys.objects.filter(used_by=request.user, is_confirmed_by_user=True, is_confirmed_by_admin=True,
                                          product=product).count()


@register.simple_tag
def has_transaction(user):
    try:
        TransactionKeys.objects.get(handler=user, is_confirmed_by_user=False,
                                    is_confirmed_by_admin=False)
        return True
    except:
        return False


@register.simple_tag
def get_ref_by_line(user, line):
    ref = user
    refs = []
    if user.related_users:
        for i in range(line):
            ref = ref.related_users
        for i in ref.all():
            refs.append(i)
    return refs


@register.simple_tag
def set_flag(flag):
    if flag == "true":
        return True
    return False
