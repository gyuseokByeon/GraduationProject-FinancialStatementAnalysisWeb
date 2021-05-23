from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from corps import models as corp_models
from . import models


def fav_corp(request, corp_code):
    action = request.GET.get("action", None)
    corp = corp_models.Corp.objects.get_or_none(corp_code=corp_code)

    if corp is not None and action is not None:
        the_list, _ = models.List.objects.get_or_create(
            user=request.user
        )

        if action == "add":
            the_list.corp.add(corp)
        elif action == "remove":
            the_list.corp.remove(corp)
    return redirect(reverse("corps:corp-detail", kwargs={"corp_code": corp_code}))



class SeeFavsView(TemplateView):

    template_name = "myCorp/myCorp.html"