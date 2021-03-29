from django.contrib import admin
from . import models


@admin.register(models.Discussion)
class DiscussionCorp(admin.ModelAdmin):
    pass