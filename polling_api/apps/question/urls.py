"""Urls."""

from django.urls import path, include

from .views import (QuestionListView,
                    QuestionView)


app_name = 'question'
urlpatterns = [
    path('', QuestionListView.as_view(), name='list'),
    path('<int:question_pk>/', QuestionView.as_view(), name='read'),
    path('<int:question_pk>/choices/', include('polling_api.apps.choice.urls')),
]
