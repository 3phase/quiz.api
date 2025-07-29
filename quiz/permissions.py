from django.contrib.auth import get_user_model
from rest_framework import permissions

from quiz.models import Invitation

User = get_user_model()


class IsQuizCreatorManagerOrInvitee(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if obj.created_by_id == request.user.id or obj.managed_by_id == request.user.id:
            return True

        return Invitation.objects.filter(
            quiz=obj,
            user=request.user,
            accepted=True
        ).exists()
