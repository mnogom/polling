"""Urls."""

from django.urls import path, include
from .views import UserView

app_name = 'user'
urlpatterns = [
    path('', UserView.as_view(), name='user'),
    path('<int:user_pk>/journal/', include('polling_api.apps.journal.urls'))
]
