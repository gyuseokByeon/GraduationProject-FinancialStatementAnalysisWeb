from django.contrib import admin
from . import models


@admin.register(models.Corp)
class CorpAdmin(admin.ModelAdmin):
    pass