import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Quiz, Score, Invitation, Question, Answer, QuestionOption

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_factory(db):
    def create_user(**kwargs):
        username = kwargs.get('username', 'user')
        password = kwargs.get('password', 'pass1234')
        return User.objects.create_user(username=username, password=password)

    return create_user


@pytest.fixture
def quiz_factory(db, user_factory):
    def create_quiz(created_by=None, managed_by=None, **kwargs):
        if created_by is None:
            created_by = user_factory(username='creator')
        quiz = Quiz.objects.create(created_by=created_by, **kwargs)
        if managed_by:
            quiz.managed_by.add(managed_by)
        return quiz

    return create_quiz


@pytest.mark.django_db
class TestQuizViewSet:
    def test_list_quizzes_for_user(self, api_client, user_factory, quiz_factory):
        user = user_factory(username='alice')
        quiz1 = quiz_factory(created_by=user, title='Math')
        quiz2 = quiz_factory(managed_by=user, title='History')
        quiz_factory(created_by=user_factory(username='bob'))

        url = reverse('quiz-list')
        api_client.force_authenticate(user=user)
        resp = api_client.get(url)

        assert resp.status_code == status.HTTP_200_OK
        titles = {q['title'] for q in resp.json()}
        assert titles == {'Math', 'History'}

    def test_scores_action(self, api_client, user_factory, quiz_factory):
        user = user_factory(username='alice')
        quiz = quiz_factory(created_by=user)
        u2 = user_factory(username='bob')
        Score.objects.create(quiz=quiz, user=u2, points=5)
        Score.objects.create(quiz=quiz, user=user, points=3)

        url = reverse('quiz-scores', kwargs={'pk': quiz.pk})
        api_client.force_authenticate(user=user)
        resp = api_client.get(url)

        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert {item['points'] for item in data} == {3, 5}


@pytest.mark.django_db
class TestInvitationViewSet:
    def test_list_and_accept_invitations(self, api_client, user_factory):
        to_user = user_factory(username='alice')
        from_user = user_factory(username='bob')
        quiz = Quiz.objects.create(created_by=to_user, title='Math')
        invitation = Invitation.objects.create(from_user=from_user, to_user=to_user, quiz=quiz)

        url = reverse('inv-list')
        api_client.force_authenticate(user=to_user)
        resp = api_client.get(url)

        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1

        url = reverse('invitation-accept', kwargs={'pk': invitation.pk})
        resp = api_client.patch(url)

        assert resp.status_code == status.HTTP_200_OK
        assert Invitation.objects.get(pk=invitation.pk).accepted == True


@pytest.mark.django_db
class TestQuestionViewSet:
    def test_crud_question(self, api_client, user_factory, quiz_factory):
        user = user_factory(username='alice')
        quiz = quiz_factory(created_by=user, title='Science')
        api_client.force_authenticate(user=user)

        url_list = reverse('question-list', kwargs={'quiz_pk': quiz.pk})
        data = {'text': 'What is 2+2?'}
        resp = api_client.post(url_list, data, format='json')
        assert resp.status_code == status.HTTP_201_CREATED
        qid = resp.json()['id']

        url_detail = reverse('question-detail', kwargs={'quiz_pk': quiz.pk, 'pk': qid})
        resp = api_client.get(url_detail)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()['text'] == data['text']

        resp = api_client.patch(url_detail, {'text': 'Updated question?'}, format='json')
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()['text'] == 'Updated question?'

        resp = api_client.delete(url_detail, format='json')
        assert resp.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestAnswerViewSet:
    def test_create_answer_updates_score(self, api_client, user_factory, quiz_factory):
        user = user_factory(username='alice')
        quiz = quiz_factory(created_by=user)
        question = Question.objects.create(quiz=quiz, text='Q?')
        opt1 = QuestionOption.objects.create(question=question, text='yes', correct=True)
        opt2 = QuestionOption.objects.create(question=question, text='no', correct=False)

        api_client.force_authenticate(user=user)
        url = reverse('answer-list')
        resp = api_client.post(url, {'question': question.pk, 'question_options': [opt1.pk, opt2.pk]}, format='json')
        assert resp.status_code == status.HTTP_201_CREATED

        score = Score.objects.get(quiz=quiz, user=user)
        assert score.points == 1


@pytest.mark.django_db
class TestScoreViewSet:
    def test_list_scores_for_user(self, api_client, user_factory, quiz_factory):
        user = user_factory(username='alice')
        quiz = quiz_factory(created_by=user)
        Score.objects.create(quiz=quiz, user=user, points=10)

        api_client.force_authenticate(user=user)
        url = reverse('score-detail')
        resp = api_client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()[0]['points'] == 10


@pytest.mark.django_db
class TestProgressViewSet:
    def test_get_progress(self, api_client, user_factory, quiz_factory):
        user = user_factory(username='alice')
        quiz = quiz_factory(created_by=user)
        q1 = Question.objects.create(quiz=quiz, text='Q1')
        q2 = Question.objects.create(quiz=quiz, text='Q2')
        Answer.objects.create(user=user, question=q1)

        api_client.force_authenticate(user=user)
        url = reverse('quiz-progress', kwargs={'quiz_pk': quiz.pk})
        resp = api_client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()['completion'] == pytest.approx(50.0)
