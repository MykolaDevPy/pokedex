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


class FavoriteObjectDetailSerializer(serializers.ModelSerializer):
    """Serializer to retreave the details of a Favorite object"""

    class Meta:
        model = FavoriteObject
        fields = "__all__"
        read_only_fields = (
            "id",
            "name",
            "img_url",
            "description",
        )
