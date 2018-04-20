from django import template

from main.models import *

register = template.Library()


@register.simple_tag
def get_refs_count(request, product):
    return TransactionKeys.objects.filter(used_by=request.user, is_confirmed=True, product=product).count()


@register.simple_tag
def has_transaction(parent_user, user):
    try:
        TransactionKeys.objects.get(handler=user, used_by=parent_user, is_confirmed=False)
        return True
    except:
        return False
