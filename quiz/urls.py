from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

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

inv_accept = InvitationViewSet.as_view({'patch': 'accept'})

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

score_detail = ScoreViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    path('get-token/', obtain_auth_token, name='api_token_auth'),
    path('quizzes/', quiz_list, name='quiz-list'),
    path('quizzes/<int:pk>/', quiz_detail, name='quiz-detail'),
    path('quizzes/<int:pk>/scores/', quiz_scores, name='quiz-scores'),
    path('invitations/', inv_list, name='inv-list'),
    path('invitations/<int:pk>/', inv_detail, name='inv-detail'),
    path('invitations/<int:pk>/accept', inv_accept, name='invitation-accept'),
    path('quizzes/<int:quiz_pk>/questions/', q_list, name='question-list'),
    path('quizzes/<int:quiz_pk>/questions/<int:pk>/', q_detail, name='question-detail'),
    path('quizzes/<int:quiz_pk>/progress/', ProgressViewSet.as_view(), name='quiz-progress'),
    path('scores/', score_detail, name='score-detail'),
]
