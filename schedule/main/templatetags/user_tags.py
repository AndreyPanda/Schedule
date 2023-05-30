from django import template

register = template.Library()

@register.filter
def is_not_string(value):
    return type(value) != str

@register.filter
def is_not_list(value):
    return type(value) != list