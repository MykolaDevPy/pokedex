from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import FavoriteObject
from .serializers import FavoriteObjectDetailSerializer
from .serializers import FavoriteObjectSerializer


@extend_schema_view(
    list=extend_schema(description="API endpoint to get a list of objects"),
    retrieve=extend_schema(
        description="API endpoint to retrieve specific object and see its details information."
    ),
)
class FavoriteObjectViewSet(ReadOnlyModelViewSet):
    # give an access to the authenticated users
    permission_classes = (IsAuthenticated,)

    # get a list of objects ordered by name
    queryset = FavoriteObject.objects.all().order_by("name")

    # serializer class
    serializer_class = FavoriteObjectSerializer

    def get_serializer_class(self):
        """Return appropriate serializer class"""

        if self.action == "list":
            return FavoriteObjectSerializer
        elif self.action == "retrieve":
            return FavoriteObjectDetailSerializer

        return super().get_serializer_class()
