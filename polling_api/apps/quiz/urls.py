"""Urls."""

from django.urls import path

from .views import (QuizzesListView,
                    QuizView)


app_name = 'quiz'
urlpatterns = [
    path('', QuizzesListView.as_view(), name='list'),
    path('<int:quiz_pk>/', QuizView.as_view(), name='read'),
]
