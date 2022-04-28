from django.db import models


class Choice(models.Model):
    """Choice model."""

    question = models.ForeignKey('question.Question',
                                 related_name='choices',
                                 on_delete=models.CASCADE)
    text = models.CharField(max_length=300,
                            blank=False,
                            null=False,
                            error_messages={
                                'blank': 'Choice text can\'t be empty',
                                'null': 'Choice text can\'t be empty',
                            })

    class Meta:
        verbose_name_plural = 'Choices'

    def __str__(self):
        return f'[{self.question}] - {self.text}'
