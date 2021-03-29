from django.shortcuts import reverse
from django.db import models
from . import managers

#재무상태표
class Financial(models.Model):
    class Meta:
        unique_together = (('code', 'date'),)


    #복합키
    code = models.ForeignKey(
        'corps.Corp', related_name='financials', on_delete=models.CASCADE
    )
    date = models.DateField()

    #총자산
    total_asset = models.BigIntegerField()

    #유동자산
    current_asset = models.BigIntegerField()

    #비유동자산
    non_current_asset = models.BigIntegerField()

    #총부채
    total_liabilities = models.BigIntegerField()

    #유동부채
    current_liabilities = models.BigIntegerField()

    #비유동부채
    non_current_liabilities = models.BigIntegerField()

    #자본
    capital = models.BigIntegerField()

    #지배기업주주지분
    controlling_share = models.BigIntegerField()

    #비지배주주지분
    non_controlling_share = models.BigIntegerField()


    objects = managers.CustomModelManager()

