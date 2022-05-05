"""Views."""

from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from .serializers import ChoiceSerializer
from .models import Choice


class ChoiceListView(ListCreateAPIView):
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(question_id=self.kwargs.get('question_pk'))

    def perform_create(self, serializer):
        serializer.save(question_id=self.kwargs.get('question_pk'))


class ChoiceView(RetrieveUpdateDestroyAPIView):
    http_method_names = ('get', 'patch', 'delete', 'head', 'options',)
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'question_pk'
