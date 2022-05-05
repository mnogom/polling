"""Views."""

import datetime

from django.db.models import Q
from rest_framework.generics import (ListAPIView,
                                     RetrieveUpdateDestroyAPIView)

from .serializers import (QuizSimpleSerializer,
                          QuizExtendedSerializer)
from .models import Quiz

ACTIVE_GROUP = 'active'


class QuizzesListView(ListAPIView):
    serializer_class = QuizSimpleSerializer
    queryset = Quiz.objects.all()

    def filter_queryset(self, queryset):
        if self.request.GET.get('group', ACTIVE_GROUP) == ACTIVE_GROUP:
            today = datetime.date.today()
            queryset = queryset.filter(
                Q(date_start__lte=today) and Q(date_end__gte=today))
        return queryset.order_by('date_start')


class QuizView(RetrieveUpdateDestroyAPIView):
    http_method_names = ('get', 'patch', 'delete', 'head', 'options',)
    serializer_class = QuizExtendedSerializer
    queryset = Quiz.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'quiz_pk'
