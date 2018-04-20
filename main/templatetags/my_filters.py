from django import template

register = template.Library()


@register.simple_tag
def get_refs_count(request, product):
    return request.user.related_users.all().filter(level=product).count()
