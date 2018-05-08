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
def get_parent_user(user, count):
    parent = user
    counter = 0
    for i in range(count):
        parent = parent.get_parent
        if parent.level.level > user.level.level:
            counter = i
            break
    return dict(parent=parent, counter=counter)


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
