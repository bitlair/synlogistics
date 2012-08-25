from django import template

register = template.Library()


@register.filter
def money_abs(value):
    if value.amount < 0:
        return -1 * value
    else:
        return value
