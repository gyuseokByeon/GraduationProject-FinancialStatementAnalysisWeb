from django.shortcuts import reverse
from django.db import models
from . import managers

class Corp(models.Model):


    corp_code = models.CharField(
        max_length=20, primary_key=True)

    corp_name = models.CharField(max_length=50)

    objects = managers.CustomModelManager()

