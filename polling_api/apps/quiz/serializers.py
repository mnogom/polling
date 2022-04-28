from rest_framework import serializers

from .models import Quiz


class QuizSimpleSerializer(serializers.ModelSerializer):
    """Quizzes serializer."""

    class Meta:
        """Meta class."""

        model = Quiz
        fields = (
            'id',
            'name',
            'date_start',
            'date_end',
            'description',
        )
