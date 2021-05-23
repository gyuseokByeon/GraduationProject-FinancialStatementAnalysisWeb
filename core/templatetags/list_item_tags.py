from django import template

register = template.Library()

@register.filter
def select_item(list, i):


    return list[i]