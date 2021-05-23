from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.views.generic import FormView, CreateView
from django.http import Http404
from django.views.generic import View
from . import models, forms
from corps import models as corp_models


def go_discussion(request, dis_pk):
    discussion = models.Discussion.objects.get_or_none(pk=dis_pk)

    return redirect(reverse("discussions:detail", kwargs={"pk": discussion.pk}))


class ConversationDetailView(View):

    model = models.Discussion
    context_object_name = "discussion"

    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        discussion = models.Discussion.objects.get_or_none(pk=pk)
        if not discussion:
            raise Http404()
        return render(
            self.request,
            "discussions/discussion_detail.html",
            {"discussion": discussion},
        )

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        discussion = models.Discussion.objects.get_or_none(pk=pk)
        if not discussion:
            raise Http404()

        if message is not None:
            models.Message.objects.create(
                message=message, user=self.request.user, discussion=discussion
            )
        return redirect(reverse("discussions:detail", kwargs={"pk": pk}))


class CreateDiscussionView(FormView):
    form_class = forms.CreateDiscussionForm
    template_name = "discussions/create_discussion.html"

    def form_valid(self, form):
        discussion = form.save()
        ##
        code = self.kwargs.get("corp_code")
        discussion.corp = corp_models.Corp.objects.get(corp_code=code)
        discussion.save()
        discussion.participants.add(self.request.user)
        form.save_m2m()
        messages.success(self.request, "Create Discussion")
        return redirect(
            reverse("corps:corp-detail", kwargs={"corp_code": discussion.corp.corp_code})
        )


def participate(request, pk):

    discussion = models.Discussion.objects.get_or_none(pk=pk)
    discussion.participants.add(request.user)

    return redirect(reverse("discussions:detail", kwargs={"corp_code": discussion.corp.corp_code}))