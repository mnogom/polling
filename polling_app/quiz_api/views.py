from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Question, Quiz, User, Choice, \
    UserQuizHistory, UserChoiceHistory
from .serializers import QuizzesSerializer, QuizDetailedSerializer, \
    UserQuizzesSerializer, DetailedUserQuizSerializer

import datetime

from .errors import QuizAPIKeysError, QuizAPIIndexError, QuizAPITypeError


class QuizzesView(APIView):
    def get(self, request, group: str):
        if group not in ('all', 'active'):
            return Response(
                {'detail': 'group must be \'all\' or \'active\''},
                status=status.HTTP_400_BAD_REQUEST
            )

        today = datetime.date.today()
        quizzes = Quiz.objects

        if group == 'all':
            quizzes = quizzes.all()

        if group == 'active':
            quizzes = quizzes.filter(date_start__lte=today)
            quizzes = quizzes.filter(date_end__gte=today)

        quizzes = quizzes.order_by('date_start')
        serializer = QuizzesSerializer(quizzes,
                                       many=True)
        return Response({'quizzes': serializer.data})


class QuizDetailedView(APIView):
    def get(self, request, quiz_id: int):
        quiz = Quiz.objects.get(pk=quiz_id)
        serializer = QuizDetailedSerializer(quiz)
        return Response(serializer.data)


class NewUserView(APIView):
    @staticmethod
    def validate_post_data(data):
        if not data:
            raise QuizAPIKeysError('data is empty')
        if {'username'} != data.keys():
            raise QuizAPIKeysError(f'data must contains "username",'
                                   f'but it contains {list(data.keys())}')

    def post(self, request):
        data = request.data
        try:
            self.validate_post_data(data)
        except QuizAPIKeysError as exception:
            return Response(
                {'detail': str(exception)},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_user = User(username=request.data['username'])
        new_user.save()
        return Response({
            'detail': 'user saved',
            'user_id': new_user.id
        })


class SaveUserQuizAnswers(APIView):

    @staticmethod
    def validate_post_data(data, user_id):  # noqa: C901

        required_keys = {'quiz_id', 'answers'}
        if set(data.keys()) != required_keys:
            raise QuizAPIKeysError('Keys in data not full')

        if not isinstance(data['answers'], list):
            raise QuizAPITypeError(f'data["answers"] must be "list"'
                                   f'but it type is {type(data["answers"])}')

        required_keys = {'choice_id', 'value'}
        for answers in data['answers']:
            if set(answers.keys()) != required_keys:
                raise QuizAPIKeysError('Keys in data not full')

        if not User.objects.filter(pk=user_id):
            raise QuizAPIIndexError('User ID not found')

        if not Quiz.objects.filter(pk=data['quiz_id']):
            raise QuizAPIIndexError('Quiz ID not found')

        user_quiz_history = UserQuizHistory.objects.filter(
            user_id=user_id)
        quiz_history_ids = [element.quiz.id for element in user_quiz_history]
        print(quiz_history_ids)
        if data['quiz_id'] in quiz_history_ids:
            raise QuizAPIKeysError(f'User {user_id} '
                                   f'already pass Quiz {data["quiz_id"]}')

        quiz_questions = Question.objects.filter(
            quiz_id=data['quiz_id'])
        quiz_questions_id = {question.id for question in quiz_questions}
        quiz_choices = Choice.objects.filter(
            question_id__in=quiz_questions_id)
        quiz_choices_id = {choice.id for choice in quiz_choices}
        data_choices = {choice['choice_id'] for choice in data['answers']}
        if quiz_choices_id != data_choices:
            raise QuizAPIIndexError('Data choices IDs doesn\'t '
                                    'similar with Question choices IDs')

        for question in quiz_questions:
            question_choices_id = [
                choice.id for choice in Choice.objects.filter(
                    question_id=question.id)]
            counter = 0
            if question.type == 1 or question.type == 2:
                for user_answers in data['answers']:
                    if user_answers['choice_id'] in question_choices_id:

                        counter += int(user_answers['value'])
                        if question.type == 1 and counter > 1:
                            raise QuizAPITypeError(f'Question ID {question.id} '
                                                   f'has only one answer')
            if counter == 0 and question.type != 3:
                raise QuizAPITypeError(f'User didn\'t answer '
                                       f'on question ID {question.id}')

    def post(self, request, user_id: int):
        try:
            self.validate_post_data(request.data, user_id)
        except (QuizAPIKeysError,
                QuizAPITypeError,
                QuizAPIIndexError) as exception:
            return Response(
                {'detail': str(exception)},
                status=status.HTTP_400_BAD_REQUEST
            )

        quiz_id = request.data['quiz_id']
        user_choices = request.data['answers']

        user_quiz_history = UserQuizHistory(user_id=user_id,
                                            quiz_id=quiz_id)

        user_choices_history = []
        for choice in user_choices:
            user_choices_history.append(
                UserChoiceHistory(user_id=user_id,
                                  choice_id=choice['choice_id'],
                                  answer=choice['value'])
            )

        user_quiz_history.save()
        for element in user_choices_history:
            element.save()
        return Response(
            {'detail': 'Quiz saved'}
        )


class UserQuizzesView(APIView):
    def get(self, request, user_id: int):
        quizzes = UserQuizHistory.objects.filter(user_id=user_id)
        serializer = UserQuizzesSerializer(quizzes,
                                           many=True)
        return Response({'quizzes': serializer.data})


class DetailedUserQuizView(APIView):

    def get(self, request, user_id: int, quiz_id: int):

        answers = UserChoiceHistory.objects
        answers = answers.filter(user_id=user_id)
        answers = answers.filter(choice__question__quiz_id=quiz_id)

        if answers:
            serializer = DetailedUserQuizSerializer(answers,
                                                    many=False)
            return Response({'quiz': serializer.data})
        return Response({'detail': f'User {user_id} didn\'t complete quiz {quiz_id}'},
                        status=status.HTTP_404_NOT_FOUND)