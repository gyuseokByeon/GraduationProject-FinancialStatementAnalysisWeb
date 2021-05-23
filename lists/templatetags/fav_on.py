from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, corp):
    user = context.request.user
    the_list = list_models.List.objects.get_or_none(
        user=user)

    if the_list is None:
        return the_list
    elif corp in the_list.corp.all():
        return the_list
    else:
        return None
