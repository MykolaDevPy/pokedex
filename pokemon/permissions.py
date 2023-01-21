from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Check if a user has the given permission"""

    def has_object_permission(self, request, view, obj):
        permission_access = False
        if request.user.is_superuser:
            permission_access = True
        else:
            permission_access = obj.trainer == request.user

        return permission_access
