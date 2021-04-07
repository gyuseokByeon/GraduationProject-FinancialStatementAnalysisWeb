from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from . import managers

#주가
class Stock(models.Model):
    class Meta:
        unique_together = (('code_id', 'date'),)


    #복합키
    code = models.ForeignKey(
        'corps.Corp', related_name='stocks', on_delete=models.CASCADE
    )
    date = models.DateField()

    datestamp = models.BigIntegerField()

    #시가
    open = models.BigIntegerField()

    #고가
    high = models.BigIntegerField()

    #저가
    low = models.BigIntegerField()

    #종가
    close = models.BigIntegerField()

    #변동량
    diff = models.BigIntegerField()

    #거래량
    volume = models.BigIntegerField()

    objects = managers.CustomModelManager()

    def __str__(self):
        return self.code.corp_name+ " " + str(self.date)
