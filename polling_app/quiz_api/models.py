"""Quiz API models."""


from django.db import models

QUESTION_TYPE = (
    (1, 'Single choice'),
    (2, 'Multiple choices'),
    (3, 'Text answer'),
)


class Quiz(models.Model):
    """Quiz model."""

    name = models.CharField(max_length=300)
    date_start = models.DateField(editable=True)
    date_end = models.DateField(editable=True)
    description = models.CharField(max_length=300)

    class Meta:
        """Meta class."""

        verbose_name_plural = '1. Quizzes'

    def __str__(self):
        """Converting method."""

        return self.name


class Question(models.Model):
    """Question model."""

    quiz = models.ForeignKey('Quiz',
                             related_name='questions',
                             on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    type = models.SmallIntegerField(choices=QUESTION_TYPE,
                                    default=3)

    class Meta:
        """Meta class."""

        verbose_name_plural = '2. Questions'

    def __str__(self):
        """Converting method."""

        return f'{self.quiz} :: {self.text}'


class Choice(models.Model):
    """Choice model."""

    question = models.ForeignKey('Question',
                                 related_name='choices',
                                 on_delete=models.CASCADE)
    text = models.CharField(max_length=300)

    class Meta:
        """Meta class."""

        verbose_name_plural = '3. Choices'

    def __str__(self):
        """Converting method."""

        return f'[{self.question}] - {self.text}'


class User(models.Model):
    """User model."""

    username = models.CharField(max_length=20)

    class Meta:
        """Meta class."""

        verbose_name_plural = '4. Users'

    def __str__(self):
        """Converting method."""

        return self.username


class UserQuizHistory(models.Model):
    """User-Quiz history model."""

    user = models.ForeignKey('User',
                             related_name='users',
                             on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz',
                             related_name='quiz',
                             on_delete=models.CASCADE)

    class Meta:
        """Meta class."""

        verbose_name_plural = '5. Completed quizzes by users'

    def __str__(self):
        """Converting method."""

        return f'"{self.quiz}" @ "{self.user}"'


class UserChoiceHistory(models.Model):
    """User-Choice history model"""

    user = models.ForeignKey('User',
                             related_name='user',
                             on_delete=models.CASCADE)
    choice = models.ForeignKey('Choice',
                               related_name='choice',
                               on_delete=models.CASCADE)
    answer = models.CharField(max_length=300)

    class Meta:
        """Meta class."""

        verbose_name_plural = '6. User choices'

    def __str__(self):
        """Converting method."""

        return f'{self.choice} : {self.answer} @ {self.user}'
