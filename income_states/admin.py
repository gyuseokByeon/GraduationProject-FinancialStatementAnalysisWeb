from django.contrib import admin
from . import models


@admin.register(models.Income)
class IncomeAdmin(admin.ModelAdmin):
    pass