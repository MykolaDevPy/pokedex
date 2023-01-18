from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Check if a user has the given permission"""

    def has_object_permission(self, request, view, obj):
        return obj == request.user
