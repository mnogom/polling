"""Admin panel."""

from django.contrib import admin
from .models import (UserQuizJournal,
                     UserChoiceJournal)


class UserQuizJournalAdmin(admin.ModelAdmin):
    pass


class UserChoiceJournalAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserQuizJournal,
                    UserQuizJournalAdmin)
admin.site.register(UserChoiceJournal,
                    UserChoiceJournalAdmin)
