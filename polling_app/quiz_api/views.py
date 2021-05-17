"""Views."""


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import QuizSerializer, QuizDetailedSerializer, \
    UserQuizzesSerializer, DetailedUserQuizSerializer

from .errors import QuizAPIKeyError, QuizAPIIndexError, QuizAPITypeError
from .services import get_grouped_quizzes, get_quiz, save_new_user, \
    get_completed_quizzes_by_user, save_users_quiz_answers, \
    get_user_answers_on_quiz


class QuizzesView(APIView):
    """Quizzes view."""

    def get(self, request):
        """Get method."""

        group = request.GET.get('group', 'active')

        try:
            quizzes = get_grouped_quizzes(group)
        except QuizAPIKeyError as exception:
            return Response({'detail': str(exception)},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = QuizSerializer(quizzes,
                                    many=True)
        return Response({'quizzes': serializer.data})


class QuizDetailedView(APIView):
    """Quiz detailed view."""

    def get(self, request, quiz_id: int):
        """Get method."""

        try:
            quiz = get_quiz(quiz_id)
        except QuizAPIIndexError as exception:
            return Response({'detail': str(exception)},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = QuizDetailedSerializer(quiz)
        return Response(serializer.data)


class NewUserView(APIView):
    """New user view."""

    def post(self, request):
        """Post method."""

        try:
            user_id = save_new_user(request.data)
        except QuizAPIKeyError as exception:
            return Response({'detail': str(exception)},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'detail': 'success',
            'user_id': user_id
        })


class UserQuizzesView(APIView):
    """User quizzes view."""

    def get(self, request, user_id: int):
        """Get method."""

        try:
            quizzes = get_completed_quizzes_by_user(user_id)
        except QuizAPIIndexError as exception:
            return Response({'detail': str(exception)},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = UserQuizzesSerializer(quizzes,
                                           many=True)
        return Response({'quizzes': serializer.data})


class DetailedUserQuizView(APIView):
    """Detailed user quiz view."""

    def get(self, request, user_id: int, quiz_id: int):
        """Get method."""

        try:
            answers = get_user_answers_on_quiz(user_id, quiz_id)
        except QuizAPIIndexError as exception:
            return Response({'detail': str(exception)},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = DetailedUserQuizSerializer(answers,
                                                many=False)
        return Response({'quiz': serializer.data})

    def post(self, request, user_id: int, quiz_id: int):
        """Post method."""

        data = request.data

        try:
            save_users_quiz_answers(user_id, quiz_id, data)
        except (QuizAPIKeyError,
                QuizAPITypeError,
                QuizAPIIndexError) as exception:
            return Response(
                {'detail': str(exception)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'detail': 'Quiz saved'}
        )
