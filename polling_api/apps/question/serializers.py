"""Serializers."""

from rest_framework import serializers

from polling_api.apps.choice.serializers import ChoiceSerializer

from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True,
                               read_only=True)
    # type = serializers.CharField(source='get_type_display')

    class Meta:
        model = Question
        fields = (
            'id',
            'text',
            'type',
            'choices',
        )
