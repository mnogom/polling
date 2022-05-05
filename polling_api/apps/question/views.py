"""Views."""

from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from .serializers import QuestionSerializer
from .models import Question


class QuestionListView(ListCreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(quiz_id=self.kwargs.get('quiz_pk'))

    def perform_create(self, serializer):
        serializer.save(quiz_id=self.kwargs.get('quiz_pk'))


class QuestionView(RetrieveUpdateDestroyAPIView):
    http_method_names = ('get', 'patch', 'delete', 'head', 'options',)
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'question_pk'
