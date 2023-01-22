from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework.viewsets import ModelViewSet

from .models import Team
from .filters import TeamsFilterSet
from .permissions import IsOwner
from .serializers import TeamSerializer
from .serializers import TeamDetailsSerializer


@extend_schema_view(
    list=extend_schema(description="API endpoint to get a list of teams of user"),
    retrieve=extend_schema(
        description="API endpoint to retrieve a specific team and its details"
    ),
    create=extend_schema(description="API endpoint to create a new team"),
    update=extend_schema(description="API endpoint to update a specific team"),
    partial_update=extend_schema(
        description="API endpoint to partially modify a specific team"
    ),
    destroy=extend_schema(description="API endpoint to delete a specific team"),
)
class TeamViewSet(ModelViewSet):
    permission_classes = (IsOwner,)
    serializer_class = TeamSerializer
    filterset_class = TeamsFilterSet

    def get_queryset(self):
        """Return the queryset of Teams instances based on user permissions."""

        if self.request.user.is_superuser:
            return Team.objects.all().order_by("name")
        return Team.objects.filter(trainer=self.request.user.pk).order_by("name")


    def get_serializer_class(self):
        if self.action == "retrieve":
            return TeamDetailsSerializer
        
        return TeamSerializer