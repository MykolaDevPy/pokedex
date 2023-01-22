import django_filters

from .models import FavoriteObject


class FavoriteObjectFilter(django_filters.FilterSet):
    """Filter for favorite objects listing."""

    id = django_filters.NumberFilter()
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = FavoriteObject
        fields = ["id", "name"]
