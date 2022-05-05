"""Urls."""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v0/users/', include('polling_api.apps.user.urls')),
    path('api/v0/quizzes/', include('polling_api.apps.quiz.urls'))
]
