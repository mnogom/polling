from django.db import models


class Quiz(models.Model):
    """Quiz model."""

    name = models.CharField(max_length=300,
                            unique=True,
                            blank=False,
                            null=False,
                            error_messages={
                                'unique': 'A quiz with that name already exists.',
                            })
    date_start = models.DateField(editable=True,
                                  blank=False,
                                  null=False,
                                  error_messages={
                                      'blank': 'Date start is not set up.',
                                      'null': 'Date start is not set up.',
                                  })
    date_end = models.DateField(editable=True,
                                blank=False,
                                null=False,
                                error_messages={
                                    'blank': 'Date end is not set up.',
                                    'null': 'Date end is not set up.',
                                })
    description = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.name
