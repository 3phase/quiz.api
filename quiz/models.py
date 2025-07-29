from django.conf import settings
from django.db import models

# Create your models here.
USER_MODEL = settings.AUTH_USER_MODEL


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quizzes_created'
    )
    managed_by = models.ManyToManyField(
        USER_MODEL,
        related_name='quizzes_managed',
        blank=True)

    class Meta:
        ordering = ['pk']


class Question(models.Model):
    text = models.TextField()
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    prev = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='next_questions'
    )
    next = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='prev_questions'
    )

    class Meta:
        ordering = ['pk']


class QuestionOption(models.Model):
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, )

    class Meta:
        ordering = ['pk']


class Invitation(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='invitations'
    )
    from_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name='invitations_sent'
    )
    to_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name='invitations_received'
    )
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('quiz', 'from_user', 'to_user')


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_options = models.ManyToManyField(QuestionOption)
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question', 'user')


class Score(models.Model):
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    points = models.FloatField(
        default=0,
    )

    class Meta:
        unique_together = ('user', 'quiz')
