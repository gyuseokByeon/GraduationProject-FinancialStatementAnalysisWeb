from django.shortcuts import reverse
from django.db import models
from . import managers

#손익계산서
class Income(models.Model):
    class Meta:
        unique_together = (('code', 'date'),)


    #복합키
    code = models.CharField(
        max_length=20)
    date = models.IntegerField()

    #매출액
    revenue = models.BigIntegerField()

    #매출원가
    cost  = models.BigIntegerField()

    #매출총이익
    gross_profit = models.BigIntegerField()

    #판관비
    operating_expense = models.BigIntegerField()

    #영업이익
    operating_profit = models.BigIntegerField()

    #금융수익
    financial_income = models.BigIntegerField(null=True)

    #당기순이익
    net_income = models.BigIntegerField()


    objects = managers.CustomModelManager()

