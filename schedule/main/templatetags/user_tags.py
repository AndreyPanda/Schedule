from django import template

register = template.Library()


@register.filter
def is_not_string(value):
    return type(value) != str


@register.filter
def is_not_list(value):
    return type(value) != list


@register.filter
def is_not_dict(value):
    return type(value) != dict
