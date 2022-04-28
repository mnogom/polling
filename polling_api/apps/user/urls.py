"""Urls."""

from django.urls import path, include

app_name = 'user'
urlpatterns = [
    path('<int:user_pk>', include('polling_api.apps.journal.urls'))
]
