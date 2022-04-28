from django.db import models


class UserQuizJournal(models.Model):
    """User-Quiz journal model."""

    user = models.ForeignKey('user.User',
                             related_name='users',
                             on_delete=models.CASCADE)
    quiz = models.ForeignKey('quiz.Quiz',
                             related_name='quiz',
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'User-Quizzes journal'

    def __str__(self):
        return f'"{self.quiz}" @ "{self.user}"'


class UserChoiceJournal(models.Model):
    """User-Choice journal model"""

    user = models.ForeignKey('user.User',
                             related_name='user',
                             on_delete=models.CASCADE)
    choice = models.ForeignKey('choice.Choice',
                               related_name='choice',
                               on_delete=models.CASCADE)
    answer = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = 'User-Choices journal'

    def __str__(self):
        return f'{self.choice} : {self.answer} @ {self.user}'
