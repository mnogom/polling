"""Services."""


from .models import Quiz, User, UserQuizHistory, \
    UserChoiceHistory, Question, Choice
from .errors import QuizAPIKeyError, QuizAPIIndexError, QuizAPITypeError

import datetime


def validate_group_quiz(group: str):
    """Check if group is approve."""

    quiz_group = ('all', 'active')

    if group not in quiz_group:
        raise QuizAPIKeyError(f'Group can be \'all\' or \'active\'. '
                              f'Your group is \'{group}\'')
    return group


def check_if_quiz_exists(quiz_id: int):
    """Check if quiz exists."""

    if not Quiz.objects.filter(pk=quiz_id):
        raise QuizAPIIndexError(f'Quiz {quiz_id} doesn\'t exists')
    return quiz_id


def check_if_user_exists(user_id: int):
    """Check if user exists."""

    if not User.objects.filter(pk=user_id):
        raise QuizAPIIndexError(f'User {user_id} doesn\'t exists')
    return user_id


def validate_username_data(data):
    """Check if data contains required information."""

    if set(data.keys()) != {'username'}:
        raise QuizAPIKeyError(f'data must contains "username",'
                              f'but it contains {list(data.keys())}')
    return data


def check_keys_in_user_answers_quiz(data):
    """Check if data contains required information."""

    required_keys = {'answers'}
    if set(data.keys()) != required_keys:
        raise QuizAPIKeyError('Keys in data not full')

    required_keys = {'choice_id', 'value'}
    for answer in data['answers']:
        if set(answer.keys()) != required_keys:
            raise QuizAPIKeyError('Keys in data not full')

    return data


def check_datatype_in_user_answers_quiz(data):
    """Check if datatype is valid."""

    if not isinstance(data['answers'], list):
        raise QuizAPITypeError(f'data["answers"] must be "list"'
                               f'but it type is {type(data["answers"])}')
    return data


def check_if_user_already_pass_quiz(user_id: int, quiz_id: int):
    """Check if user already pass quiz."""

    user_quiz_history = UserQuizHistory.objects
    user_quiz_history = user_quiz_history.filter(user_id=user_id)
    user_quiz = user_quiz_history.filter(quiz_id=quiz_id)

    if not user_quiz:
        raise QuizAPIKeyError(f'User {user_id} '
                              f'already pass Quiz {quiz_id}')
    return user_id, quiz_id


def check_if_choices_is_linked_with_quiz(data, quiz_id: int):
    """Check if choice is linked with quiz."""

    quiz_questions = Question.objects.filter(
        quiz_id=quiz_id)
    quiz_questions_id = {question.id for question in quiz_questions}
    quiz_choices = Choice.objects.filter(
        question_id__in=quiz_questions_id)
    quiz_choices_id = {choice.id for choice in quiz_choices}
    data_choices = {choice['choice_id'] for choice in data['answers']}
    if quiz_choices_id != data_choices:
        raise QuizAPIIndexError('Data choices IDs doesn\'t '
                                'similar with Question choices IDs')
    return data


def check_if_questions_type_rules_are_performed(data, quiz_id: int):  # noqa: C901, E501
    """Check if question type rules are performed by user answers."""

    quiz_questions = Question.objects.filter(
        quiz_id=quiz_id)
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

    return data


def get_grouped_quizzes(group: str):
    """Get all grouped quizzes."""

    group = validate_group_quiz(group)

    today = datetime.date.today()
    quizzes = Quiz.objects

    if group == 'all':
        quizzes = quizzes.all()

    elif group == 'active':
        quizzes = quizzes.filter(date_start__lte=today)
        quizzes = quizzes.filter(date_end__gte=today)

    return quizzes.order_by('date_start')


def get_quiz(quiz_id: int):
    """Get quiz by id."""

    quiz_id = check_if_quiz_exists(quiz_id)
    return Quiz.objects.get(pk=quiz_id)


def save_new_user(data):
    """Save new user."""

    data = validate_username_data(data)
    new_user = User(username=data['username'])
    new_user.save()
    return new_user.id


def get_completed_quizzes_by_user(user_id: int):
    """Get set of completed quizzes by user."""

    user_id = check_if_user_exists(user_id)
    return UserQuizHistory.objects.filter(user_id=user_id)


def save_users_quiz_answers(user_id: int, quiz_id: int, data):
    """Save users answers on quiz."""

    user_id = check_if_user_exists(user_id)
    quiz_id = check_if_quiz_exists(quiz_id)
    user_id, quiz_id = check_if_user_already_pass_quiz(user_id, quiz_id)
    data = check_datatype_in_user_answers_quiz(data)
    data = check_keys_in_user_answers_quiz(data)
    data = check_if_choices_is_linked_with_quiz(data, quiz_id)
    data = check_if_questions_type_rules_are_performed(data, quiz_id)

    choices_ids = [answer['choice_id'] for answer in data['answers']]
    user_answers = [answer['value'] for answer in data['answers']]

    user_quiz_history = UserQuizHistory(user_id=user_id,
                                        quiz_id=quiz_id)
    user_choices_history = []
    for choice_id, answer in zip(choices_ids, user_answers):
        user_choices_history.append(
            UserChoiceHistory(user_id=user_id,
                              choice_id=choice_id,
                              answer=answer)
        )

    user_quiz_history.save()
    for element in user_choices_history:
        element.save()


def get_user_answers_on_quiz(user_id: int, quiz_id: int):
    """Get users answers on quiz."""

    user_id = check_if_user_exists(user_id)
    quiz_id = check_if_quiz_exists(quiz_id)

    answers = UserChoiceHistory.objects
    answers = answers.filter(user_id=user_id)
    answers = answers.filter(choice__question__quiz_id=quiz_id)
    if not answers:
        raise QuizAPIIndexError(f'User {user_id} didn\'t '
                                f'complete quiz {quiz_id}')
    return answers
