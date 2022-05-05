"""Models."""

from django.db import models


class UserChoiceJournal(models.Model):
    """User-Choice journal model."""

    user = models.ForeignKey('user.User',
                             related_name='user_choices',
                             on_delete=models.CASCADE)
    choice = models.ForeignKey('choice.Choice',
                               related_name='user_journal',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=False)
    answer = models.CharField(max_length=300,
                              null=True,
                              blank=False)

    class Meta:
        verbose_name_plural = 'User choices journal'

    def __str__(self):
        return f'{self.choice} : {self.answer} @ {self.user}'


class UserQuizJournal(models.Model):
    """User-Quiz journal model."""

    user = models.ForeignKey('user.User',
                             related_name='user_quizzes',
                             on_delete=models.CASCADE)
    quiz = models.ForeignKey('quiz.Quiz',
                             related_name='user_journal',
                             on_delete=models.CASCADE)
