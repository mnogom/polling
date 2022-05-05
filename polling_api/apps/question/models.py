from django.db import models

SINGLE_CHOICE = 1
MULTIPLE_CHOICES = 2
TEXT_ANSWER = 3

QUESTION_TYPE = (
    (SINGLE_CHOICE, 'Single choice'),
    (MULTIPLE_CHOICES, 'Multiple choices'),
    (TEXT_ANSWER, 'Text answer'),
)


class Question(models.Model):
    """Question model."""

    quiz = models.ForeignKey('quiz.Quiz',
                             related_name='questions',
                             on_delete=models.CASCADE)
    text = models.CharField(max_length=300,
                            blank=False,
                            null=False,
                            error_messages={
                                'blank': 'Question text can\'t be empty',
                                'null': 'Question text can\'t be empty',
                            })
    type = models.SmallIntegerField(choices=QUESTION_TYPE,
                                    default=TEXT_ANSWER)

    class Meta:
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.text
