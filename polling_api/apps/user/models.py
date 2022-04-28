from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(models.Model):
    """Simple user model."""

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(max_length=20,
                                unique=True,
                                blank=False,
                                null=False,
                                validators=[username_validator],
                                error_messages={
                                    'unique': 'A user with that username already exists.',
                                })

    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
