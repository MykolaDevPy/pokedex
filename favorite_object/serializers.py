from rest_framework import serializers

from .models import FavoriteObject


class FavoriteObjectSerializer(serializers.ModelSerializer):
    """Serializer for FavoriteObject"""

    class Meta:
        model = FavoriteObject
        fields = (
            "name",
            "img_url",
        )
        read_only_fields = (
            "id",
            "description",
        )


class FavoriteObjectDetailSerializer(serializers.ModelSerializer):
    """Serializer to retreave the details of a Favorite object"""

    class Meta:
        model = FavoriteObject
        fields = (
            "name",
            "img_url",
            "description",
        )
        read_only_fields = ("id",)
