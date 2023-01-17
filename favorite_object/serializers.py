from rest_framework import serializers

from .models import FavoriteObject


class FavoriteObjectSerializer(serializers.ModelSerializer):
    """Serializer for FavoriteObject"""

    class Meta:
        model = FavoriteObject
        fields = (
            "id",
            "name",
            "img_url",
            "description",
        )
        read_only_fields = (
            "id",
            "name",
            "img_url",
            "description",
        )
