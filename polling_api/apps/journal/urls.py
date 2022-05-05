"""Urls."""

from django.urls import path

from .views import (JournalQuizList,
                    JournalChoicesList)

app_name = 'journal'
urlpatterns = [
    path('quizzes/', JournalQuizList.as_view(), name='quiz-list'),
    path('quizzes/<int:quiz_pk>/', JournalChoicesList.as_view(), name='choices-list')
]
