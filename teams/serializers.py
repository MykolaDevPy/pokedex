from rest_framework.serializers import ModelSerializer

from .models import Team
from authentication.serializers import UserSerializer


class TeamSerializer(ModelSerializer):
    """Serializer for Team instances"""

    class Meta:
        model = Team
        fields = "__all__"
        read_only_fields = ("id", "trainer")
