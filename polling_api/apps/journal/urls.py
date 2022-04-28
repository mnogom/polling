"""Urls."""

from django.urls import path

from .views import (QuizJournalQuizList,
                    QuizJournalChoicesList)

app_name = 'journal'
urlpatterns = [
    path('journal/quizzes/', QuizJournalQuizList.as_view(), name='quiz-list'),
    path('journal/quizzes/<int:quiz_pk>/', QuizJournalChoicesList.as_view(), name='choices-list')
]
