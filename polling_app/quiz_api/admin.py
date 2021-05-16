"""Admin panel."""

from django.contrib import admin

from .models import User, Quiz, Question, Choice, \
    UserQuizHistory, UserChoiceHistory


class MyModelAdmin(admin.ModelAdmin):
    """Custom admin model."""

    def get_readonly_fields(self, request, obj=None):
        """Edit readonly fields."""

        if obj:
            return self.readonly_fields + ('date_start', )
        return self.readonly_fields


admin.site.register(User)
admin.site.register(Quiz, MyModelAdmin)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UserQuizHistory)
admin.site.register(UserChoiceHistory)
