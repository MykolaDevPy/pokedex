from django_filters import rest_framework as filters

from .models import Team


class TeamsFilterSet(filters.FilterSet):
    """Filters for teams."""

    id = filters.NumberFilter(field_name="id")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Team
        fields = ["id", "name"]
