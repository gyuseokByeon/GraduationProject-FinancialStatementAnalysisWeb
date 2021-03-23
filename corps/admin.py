from django.contrib import admin


from . import models

@admin.register(models.Corp)
class CustomUserAdmin(admin.ModelAdmin):
    pass
