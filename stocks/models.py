from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from . import managers

class Corp(models.Model):
    class Meta:
        unique_together = (('code', 'date'),)


    #복합키
    code = models.CharField(max_length=20)
    date = models.DateField()

    #속성들
    open = models.BigIntegerField()
    high = models.BigIntegerField()
    low = models.BigIntegerField()
    close = models.BigIntegerField()
    diff = models.BigIntegerField()
    volume = models.BigIntegerField()

    objects = managers.CustomModelManager()