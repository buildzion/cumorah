from django import template

from cumorah.home.models import MenuLink

register = template.Library()


@register.simple_tag(takes_context=False)
def cumorah_menu():
    qs = MenuLink.objects.filter(active=True)
    return list(qs)
