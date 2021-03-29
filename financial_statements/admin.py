from django.contrib import admin
from . import models


@admin.register(models.Financial)
class FinancialAdmin(admin.ModelAdmin):
    pass