from django.urls import path

from .views import QuizViewSet, InvitationViewSet, QuestionViewSet, AnswerViewSet, ScoreViewSet, ProgressViewSet

quiz_list = QuizViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

quiz_detail = QuizViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

quiz_scores = QuizViewSet.as_view({'get': 'scores'})

inv_list = InvitationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

inv_detail = InvitationViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

q_list = QuestionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

q_detail = QuestionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

ans_list = AnswerViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

ans_detail = AnswerViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

score_detail = ScoreViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    path('users/<int:user_pk>/quizzes/', quiz_list, name='quiz-list'),
    path('users/<int:user_pk>/quizzes/<int:pk>/', quiz_detail, name='quiz-detail'),
    path('users/<int:user_pk>/quizzes/<int:pk>/scores/', quiz_scores, name='quiz-scores'),
    path('users/<int:user_pk>/invitations/', inv_list, name='inv-list'),
    path('users/<int:user_pk>/invitations/<int:pk>/', inv_detail, name='inv-detail'),
    path('users/<int:user_pk>/quizzes/<int:quiz_pk>/questions/', q_list, name='question-list'),
    path('users/<int:user_pk>/quizzes/<int:quiz_pk>/questions/<int:pk>/', q_detail, name='question-detail'),
    path('users/<int:user_pk>/answers/', ans_list, name='answer-list'),
    path('users/<int:user_pk>/answers/<int:pk>/', ans_detail, name='answer-detail'),
    path('users/<int:user_pk>/scores/', score_detail, name='score-detail'),
    path('users/<int:user_pk>/quizzes/<int:quiz_pk>/progress/', ProgressViewSet.as_view(), name='quiz-progress'),
]
