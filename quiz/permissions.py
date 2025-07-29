from django.contrib.auth import get_user_model
from rest_framework import permissions

from quiz.models import Invitation

User = get_user_model()


class IsQuizCreatorManagerOrInvitee(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user_pk = view.kwargs.get('user_pk')
        if not user_pk:
            return False

        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return False

        if obj.created_by_id == user.id or obj.managed_by_id == user.id:
            return True

        return Invitation.objects.filter(
            quiz=obj,
            user=user,
            accepted=True
        ).exists()
