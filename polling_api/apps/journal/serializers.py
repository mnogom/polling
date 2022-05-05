"""Serializers."""

from rest_framework import serializers

from polling_api.apps.quiz.serializers import QuizSimpleSerializer
from polling_api.apps.user.serializers import UserSimpleSerializer

from .models import (UserQuizJournal,
                     UserChoiceJournal)


class UserDetailedQuizSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
    quiz = QuizSimpleSerializer()

    class Meta:
        model = UserQuizJournal
        fields = (
            'user',
            'quiz',
        )


class UserSimpleQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuizJournal
        fields = (
            'user',
            'quiz',
        )


class UserChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChoiceJournal
        fields = (
            'id',
            'choice',
            'answer',
        )
