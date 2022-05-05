"""Serializers."""

from rest_framework import serializers

from polling_api.apps.question.serializers import QuestionSerializer

from .models import Quiz


class QuizSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = (
            'id',
            'name',
            'date_start',
            'date_end',
            'description',
        )


class QuizExtendedSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True,
                                   read_only=True)

    class Meta:
        model = Quiz
        fields = (
            'id',
            'name',
            'date_start',
            'date_end',
            'description',
            'questions',
        )
