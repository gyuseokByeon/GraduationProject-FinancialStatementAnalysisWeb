from django.contrib.auth.models import AbstractUser
from django.db import models
from . import managers

#주가
class Stock(models.Model):
    class Meta:
        unique_together = (('code_id', 'date'),)


    date = models.DateField()

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

    # 복합키
    code_id = models.CharField(
        max_length=20)

    datestamp = models.BigIntegerField(null=True)

    objects = managers.CustomModelManager()

    def __str__(self):
        return self.code.corp_name+ " " + str(self.date)