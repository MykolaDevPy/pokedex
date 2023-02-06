import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from pokemon.models import Pokemon
from teams.models import Team
from teams.serializers import TeamSerializer

pytestmark = pytest.mark.django_db


def test_listing_teams(
        team_factory,
        user_log,
        client_log,
        client_admin,
    ):
    """Test retrieveng the teams"""

    team_factory()
    team_factory()
    team_factory(trainer=user_log)

    # Unauthenticated users should be denied access
    res = APIClient().get(reverse("teams:teams-list"))
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

    # Authenticated regular user sees only owne teams
    res = client_log.get(reverse("teams:teams-list"))
    assert res.status_code == status.HTTP_200_OK

    user_teams = Team.objects.filter(trainer=user_log.id)
    serializer = TeamSerializer(user_teams, many=True)
    
    assert res.status_code == status.HTTP_200_OK
    assert len(serializer.data) == 1
    assert serializer.data == res.data["results"]

    # Super user sees all teams
    res = client_admin.get(reverse("teams:teams-list"))
    assert res.status_code == status.HTTP_200_OK

    all_teams = Team.objects.all()
    serializer = TeamSerializer(all_teams, many=True)
    
    assert res.status_code == status.HTTP_200_OK
    assert len(serializer.data) == 3
    assert serializer.data == res.data["results"]


def test_create_team(team_factory, pokemon_factory, user_log, client_log):
    """Test creating a team by authenticated user"""
    team = team_factory()
    user = user_log

    playload = {
        "name": "My team",
        "trainer": user.id,
    }

    res = client_log.post(
        reverse("teams:teams-list"),
        playload,
        format="json",
    )
    assert res.status_code == status.HTTP_201_CREATED

    pokemon_1 = pokemon_factory(nickname="Pikachu", trainer=user, team=team)
    pokemon_2 = pokemon_factory(nickname="Charmander", trainer=user, team=team)
    pokemon_3 = pokemon_factory(nickname="Squirtle", trainer=user, team=team)

    pokemon = Pokemon.objects.get(id=pokemon_1.id)
    assert pokemon.team == team
    pokemon = Pokemon.objects.get(id=pokemon_2.id)
    assert pokemon.team == team
    pokemon = Pokemon.objects.get(id=pokemon_3.id)
    assert pokemon.team == team

  
def test_partial_update_team(
        team_factory,
        user_log,
        client_log,
    ):
    """Test partial updating a team by authenticated user"""

    user = user_log

    team = team_factory(
        name="My team",
        trainer=user,
    )

    playload = {
        "name":"My favorite team",
    }
        
    res = client_log.patch(
        reverse("teams:teams-detail", kwargs={"pk": team.id}),
        playload,
        format="json",
    )

    assert res.status_code == status.HTTP_200_OK
    team.refresh_from_db()
    assert team.name == "My favorite team"


def test_full_update_team(team_factory, user_admin, user_log, client_log):
    """Test updating a team by authenticated user"""
    user = user_log
    
    team = team_factory(
        name="My team",
        trainer=user,

    )

    playload = {
        "name": "My best team",
        "trainer": user_admin.id,
    }

    res = client_log.put(
        reverse("teams:teams-detail", kwargs={"pk": team.id}),
        playload,
        format="json",
    )

    assert res.status_code == status.HTTP_200_OK
    team.refresh_from_db()
    assert team.name == "My best team"
    assert team.trainer == user_admin


def test_delete_team(
        team_factory,
        pokemon_factory,
        user_log,
        client_log
    ):
    """
    Delete a team and check if it put 'team" and 'team_pk' of 
    pokemons to None.
    """
    user = user_log

    team = team_factory(
        name="My team",
        trainer=user,
    )

    pokemon_factory(trainer=user, team=team)
    pokemon_factory(trainer=user, team=team)
    pokemon_factory(trainer=user, team=team)
    

    res = client_log.delete(reverse("teams:teams-detail", kwargs={"pk": team.id}))
    assert res.status_code == status.HTTP_204_NO_CONTENT

    pokemons = Pokemon.objects.filter(team=team.id)
    for pokemon in pokemons:
        assert pokemon.team == None

                                  
