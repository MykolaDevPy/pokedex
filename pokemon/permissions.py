from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class IsOwner(IsAuthenticated):
    """Check if a user has the given permission"""

    def has_object_permission(self, obj, view, request):
        if obj.trainer == request.user or request.user.is_superuser:
            return True
        else:
            raise PermissionDenied
