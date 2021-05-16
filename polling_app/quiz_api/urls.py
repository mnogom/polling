"""Urls routing."""


from django.urls import path

from .views import QuizzesView, QuizDetailedView, NewUserView, \
    UserQuizzesView, DetailedUserQuizView


urlpatterns = [
    path('quizzes',
         QuizzesView.as_view()),
    path('quizzes/<int:quiz_id>',
         QuizDetailedView.as_view()),
    path('users',
         NewUserView.as_view()),
    path('users/<int:user_id>/quizzes',
         UserQuizzesView.as_view()),
    path('users/<int:user_id>/quizzes/<int:quiz_id>',
         DetailedUserQuizView.as_view()),
]
