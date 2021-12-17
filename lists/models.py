from django.shortcuts import reverse
from django.db import models
from . import managers

#내 기업 리스트
class List(models.Model):

    user = models.OneToOneField(
        "users.User", related_name="lists", on_delete=models.CASCADE
    )

    corp = models.ManyToManyField("corps.Corp", blank=True)

    objects = managers.CustomModelManager()