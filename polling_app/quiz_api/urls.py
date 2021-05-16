from django.urls import path

from .views import QuizzesView, QuizDetailedView, NewUserView, \
    SaveUserQuizAnswers, UserQuizzesView, DetailedUserQuizView


urlpatterns = [
    path('quizzes/<str:group>',
         QuizzesView.as_view()),
    path('quiz/<int:quiz_id>',
         QuizDetailedView.as_view()),
    path('user/new',
         NewUserView.as_view()),
    path('user/<int:user_id>/save_answers',
         SaveUserQuizAnswers.as_view()),
    path('user/<int:user_id>/quizzes',
         UserQuizzesView.as_view()),
    path('user/<int:user_id>/quiz/<int:quiz_id>',
         DetailedUserQuizView.as_view()),
]
