from django.shortcuts import reverse
from django.db import models
from . import managers

class Income(models.Model):
    class Meta:
        unique_together = (('code', 'date'),)


    #복합키
    code = models.CharField(max_length=20)
    date = models.DateField()

    revenue = models.BigIntegerField()
    cost  = models.BigIntegerField()
    gross_profit = models.BigIntegerField()
    operating_expense = models.BigIntegerField()
    operating_profit = models.BigIntegerField()
    financial_profit = models.BigIntegerField()
    other_income = models.BigIntegerField()




    objects = managers.CustomModelManager()

