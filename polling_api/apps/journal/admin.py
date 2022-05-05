"""Admin panel."""

from django.contrib import admin
from .models import UserChoiceJournal


class UserChoiceJournalAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserChoiceJournal,
                    UserChoiceJournalAdmin)
