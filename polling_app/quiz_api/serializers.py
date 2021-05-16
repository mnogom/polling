"""Serializers."""


from rest_framework import serializers

from .models import Quiz, Question, Choice, UserQuizHistory, UserChoiceHistory


class ChoiceSerializer(serializers.ModelSerializer):
    """Choice serializer."""

    class Meta:
        """Meta class."""

        model = Choice
        fields = (
            'id',
            'text',
        )


class QuestionSerializer(serializers.ModelSerializer):
    """Question serializer."""

    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        """Meta class."""

        model = Question
        fields = (
            'id',
            'text',
            'type',
            'choices',
        )


class QuizSerializer(serializers.ModelSerializer):
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


class QuizDetailedSerializer(serializers.ModelSerializer):
    """Detailed Quiz serializer."""

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        """Meta class."""

        model = Quiz
        fields = (
            'id',
            'name',
            'date_start',
            'date_end',
            'description',
            'questions',
        )


class UserQuizzesSerializer(serializers.ModelSerializer):
    """User-Quizzes serializer."""

    quiz_text = serializers.CharField(source='quiz.name')
    id = serializers.CharField(source='quiz.id')

    class Meta:
        """Meta class."""

        model = UserQuizHistory
        fields = (
            'id',
            'quiz_text',
        )


class DetailedUserQuizSerializer(serializers.ModelSerializer):
    """Detailed User-Quiz serializer."""

    class Meta:
        """Meta class."""

        model = UserChoiceHistory
        fields = '__all__'

    def to_representation(self, instance):
        """Representation method."""

        quiz_id = instance[0].choice.question.quiz.id
        quiz_name = instance[0].choice.question.quiz.name

        custom_data = {'id': quiz_id,
                       'name': quiz_name,
                       'question': []}

        questions_ids = []
        for element in instance:
            question_id = element.choice.question.id
            question_text = element.choice.question.text

            if question_id not in questions_ids:
                questions_ids.append(question_id)
                custom_data['question'].append(
                    {'id': question_id,
                     'text': question_text,
                     'choices': []}
                )

            choice_id = element.choice.id
            choice_text = element.choice.text
            answer = element.answer

            custom_data['question'][-1]['choices'].append({
                'id': choice_id,
                'text': choice_text,
                'answer': answer
            })

        return custom_data
