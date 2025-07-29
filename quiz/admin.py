from django.contrib import admin

from .models import Quiz, Question, Answer, QuestionOption


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'question_list')
    list_filter = ('title',)
    search_fields = ('title',)

    def question_list(self, obj):
        return ", ".join(q.text for q in obj.questions.all())


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'text')
    list_filter = ('quiz',)
    search_fields = ('text',)


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('get_question_text', 'text', 'correct')
    list_filter = ('question', 'text')
    search_fields = ('text',)

    def get_question_text(self, obj):
        return obj.question.text


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('get_question_text', 'get_question_options')
    list_filter = ('question',)

    def get_question_text(self, obj):
        return obj.question.text

    def get_question_options(self, obj):
        return ", ".join(answer.text for answer in obj.question_options.all())
