from django.shortcuts import reverse
from django.db import models
from . import managers

#기업토론
class Discussion(models.Model):

    #참여자
    participants = models.ManyToManyField(
        "users.User", related_name="discussions", blank=True
    )

    #기업
    corp = models.ForeignKey(
        "corps.Corp", related_name="discussions", on_delete=models.CASCADE
    )

    #주제
    topic = models.CharField(max_length=300)

    objects = managers.CustomModelManager()