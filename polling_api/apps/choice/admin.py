"""Admin panel."""

from django.contrib import admin
from .models import Choice


class ChoiceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Choice, ChoiceAdmin)