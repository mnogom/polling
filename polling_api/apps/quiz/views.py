"""Views."""
import datetime

from rest_framework.views import APIView
from rest_framework.generics import (ListAPIView,
                                     RetrieveAPIView)

from .serializers import QuizSimpleSerializer
from .models import Quiz

ACTIVE_GROUP = 'active'


class QuizzesListView(ListAPIView):
    serializer_class = QuizSimpleSerializer
    queryset = Quiz.objects.all()

    def filter_queryset(self, queryset):
        if self.request.GET.get('group', ACTIVE_GROUP) == ACTIVE_GROUP:
            queryset = queryset.filter(date_start__lte=datetime.date.today())
            queryset = queryset.filter(date_end__gte=datetime.date.today())
        return queryset.order_by('date_start')


class QuizView(RetrieveAPIView):
    serializer_class = QuizSimpleSerializer
    queryset = Quiz.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'quiz_pk'
