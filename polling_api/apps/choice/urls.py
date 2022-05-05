"""Urls."""

from django.urls import path

from .views import (ChoiceListView,
                    ChoiceView)


app_name = 'choice'
urlpatterns = [
    path('', ChoiceListView.as_view(), name='list'),
    path('<int:question_pk>/', ChoiceView.as_view(), name='read'),
]
