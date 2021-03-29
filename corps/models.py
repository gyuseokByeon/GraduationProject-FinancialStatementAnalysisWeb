from django.shortcuts import reverse
from django.db import models
from . import managers

#기업
class Corp(models.Model):

    #기업코드 (CharField or Int)
    corp_code = models.CharField(
        max_length=20, primary_key=True)

    #기업명
    corp_name = models.CharField(max_length=50)


    objects = managers.CustomModelManager()

