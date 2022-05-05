"""Views."""

from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from .serializers import (UserChoicesSerializer,
                          UserDetailedQuizSerializer,
                          UserSimpleQuizSerializer)
from .models import (UserChoiceJournal,
                     UserQuizJournal)


class JournalQuizList(ListCreateAPIView):
    serializer_class = UserDetailedQuizSerializer
    queryset = UserQuizJournal.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.serializer_class = UserSimpleQuizSerializer
        else:
            self.serializer_class = UserDetailedQuizSerializer
        return super().get_serializer_class()

    def filter_queryset(self, queryset):
        return queryset.filter(user_id=self.kwargs.get('user_pk'))


class JournalChoicesList(ListCreateAPIView):
    serializer_class = UserChoicesSerializer
    queryset = UserChoiceJournal.objects.all()

    def filter_queryset(self, queryset):
        queryset = queryset.filter(choice__question__quiz_id=self.kwargs.get('quiz_pk'))
        return queryset.filter(user_id=self.kwargs.get('user_pk'))

    def perform_create(self, serializer):
        serializer.save(user_id=self.kwargs.get('user_pk'))