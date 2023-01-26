import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from teams.models import Team
from teams.serializers import TeamSerializer

pytestmark = pytest.mark.django_db


def test_listing_teams(
        team_factory,
        user_log,
        client_log,
        client_admin,
    ):
    """Test listing teams"""

    team_factory()
    team_factory()
    team_factory(trainer=user_log)

    # Unauthenticated users should not be able to see any teams
    res = APIClient().get(reverse("teams:team-list"))
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Authenticated regular user see only owne teams
    res = client_log.get(reverse("teams:team-list"))
    assert res.status_code == status.HTTP_200_OK

    user_teams = Team.objects.filter(trainer=user_log)
    serializer = TeamSerializer(user_teams, many=True)
    
    assert res.status_code == status.HTTP_200_OK
    assert len(serializer.data) == 1
    assert serializer.data == res.data.get["results"]

    # Authenticated admin see all teams
    res = client_admin.get(reverse("teams:team-list"))
    assert res.status_code == status.HTTP_200_OK

    all_teams = Team.objects.all()
    serializer = TeamSerializer(all_teams, many=True)
    
    assert res.status_code == status.HTTP_200_OK
    assert len(serializer.data) == 3
    assert serializer.data == res.data.get["results"]
    




    
