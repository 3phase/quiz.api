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
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
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

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['pk']


class QuestionOption(models.Model):
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='options'
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Question Option'
        verbose_name_plural = 'Question Options'
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

    def __str__(self):
        return f"Invitation({self.quiz}, from={self.from_user}, to={self.to_user})"

    class Meta:
        unique_together = ('quiz', 'from_user', 'to_user')
        verbose_name = 'Invitation'
        verbose_name_plural = 'Invitations'


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question_options = models.ManyToManyField(
        QuestionOption,
        related_name='answers'
    )
    user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    def __str__(self):
        return f"Answer by {self.user} to Q{self.question.id}"

    class Meta:
        unique_together = ('question', 'user')
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class Score(models.Model):
    user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scores'
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='scores'
    )
    points = models.FloatField()

    def __str__(self):
        return f"Score({self.user}, {self.quiz}) = {self.points}"

    class Meta:
        unique_together = ('user', 'quiz')
        verbose_name = 'Score'
        verbose_name_plural = 'Scores'
