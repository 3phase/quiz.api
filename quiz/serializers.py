from rest_framework import serializers

from .models import Question, QuestionOption, Quiz, Answer, Invitation, Score
from .validators import OptionsBelongToQuestionValidator


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['id', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, read_only=True)
    next = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'options', 'next']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField()
    managed_by = serializers.StringRelatedField(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'created_by', 'managed_by', 'questions']


class InvitationSerializer(serializers.ModelSerializer):
    accepted = serializers.BooleanField()
    from_user = serializers.StringRelatedField()
    to_user = serializers.StringRelatedField()

    class Meta:
        model = Invitation
        fields = ['id', 'accepted', 'quiz', 'from_user', 'to_user']


class AnswerSerializer(serializers.ModelSerializer):
    question_options = serializers.PrimaryKeyRelatedField(
        queryset=QuestionOption.objects.all(),
        many=True
    )

    class Meta:
        model = Answer
        fields = ['id', 'question', 'question_options']
        validators = [
            OptionsBelongToQuestionValidator('question', 'questionOption')
        ]


class ScoreSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Score
        fields = ['quiz', 'user', 'points']
