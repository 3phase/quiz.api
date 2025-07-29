from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets, views
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Quiz, Score, Invitation, Question, Answer
from .permissions import IsQuizCreatorManagerOrInvitee, \
    UserHasPermissionsForAnswer, UserHasPermissionsForQuestion
from .serializers import QuizSerializer, ScoreSerializer, InvitationSerializer, QuestionSerializer, AnswerSerializer

User = get_user_model()


class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer

    permission_classes = [IsAuthenticated, IsQuizCreatorManagerOrInvitee]

    def get_queryset(self):
        return Quiz.objects.filter(
            Q(created_by=self.request.user) |
            Q(managed_by=self.request.user)
        ).distinct()

    @action(detail=True, methods=['get'])
    def scores(self, request, pk=None):
        qs = Score.objects.filter(quiz_id=pk)
        return Response(ScoreSerializer(qs, many=True).data)


class InvitationViewSet(viewsets.ModelViewSet):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # invitations sent to me
        return Invitation.objects.filter(to_user=self.request.user)

    def get_invitation(self, invitation_pk):
        return get_object_or_404(Invitation, pk=invitation_pk, to_user=self.request.user)

    @action(detail=True, methods=['patch'])
    def accept(self, request, pk=None):
        invitation = self.get_invitation(pk)
        invitation.accepted = True
        invitation.save()
        return Response({'accepted': True})


# these are the questions to a given quiz
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, UserHasPermissionsForQuestion]

    def get_quiz(self):
        return get_object_or_404(Quiz, pk=self.kwargs['quiz_pk'])

    def perform_create(self, serializer):
        quiz = self.get_quiz()
        serializer.save(quiz=quiz)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, UserHasPermissionsForAnswer]

    def perform_create(self, serializer):
        ans = serializer.save(user=self.request.user)
        correct_count = ans.question_options.filter(correct=True).count()
        score, _ = Score.objects.get_or_create(
            quiz=ans.question.quiz, user=self.request.user
        )
        score.points += correct_count
        score.save()


class ScoreViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Score.objects.filter(user=self.request.user)


class ProgressViewSet(views.APIView):
    permission_classes = [IsAuthenticated, IsQuizCreatorManagerOrInvitee]

    def get_quiz(self):
        return get_object_or_404(Quiz, pk=self.kwargs['quiz_pk'])

    def get(self, request, quiz_pk, *args, **kwargs):
        quiz = self.get_quiz()

        total_answers = Answer.objects.filter(
            user=self.request.user,
            question__quiz=quiz,
        ).count()

        quiz_questions = Question.objects.filter(
            quiz=quiz
        ).count()

        return Response({"completion": 100 * total_answers / quiz_questions})
