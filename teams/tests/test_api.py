import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from time import sleep

from pokemon.models import Pokemon
from teams.models import Team
from teams.serializers import TeamSerializer
from teams.serializers import TeamDetailsSerializer


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


def test_create_team(user_factory, team_factory, pokemon_factory, user_log, client_log):
    """Test creating a team by authenticated user"""
    team_factory()
    user = user_log
    pokemon_1 = pokemon_factory(nickname="Pikachu", trainer=user)
    pokemon_2 = pokemon_factory(nickname="Charmander", trainer=user)
    pokemon_3 = pokemon_factory(nickname="Squirtle", trainer=user)
    
    
    playload = {
        "name": "My team",
        "trainer": user.id,
        "pokemon_1": pokemon_1.id,
        "pokemon_2": pokemon_2.id,
        "pokemon_3": pokemon_3.id,
        "pokemon_4": "",
        "pokemon_5": "",
    }

    res = client_log.post(
        reverse("teams:teams-list"),
        playload,
        format="json",
    )
    assert res.status_code == status.HTTP_201_CREATED

    team = Team.objects.get(id=res.data.get("id"))
    assert str(team) == f"Team 'My team' (by {user.username}): Pikachu, Charmander, Squirtle."

    for i in range(1, 4):
        poke_field = f"pokemon_{i}"
        pokemon = Pokemon.objects.get(id=res.data.get(poke_field))
        assert pokemon.team == team.name
        assert pokemon.team_pk == team.id

  
def test_partial_update_team(
        team_factory,
        pokemon_factory,
        user_log,
        client_log
    ):
    """Test partial updating a team by authenticated user"""

    user = user_log
    pokemon_team = [pokemon_factory(trainer=user) for i in range(3)]
    another_pokemon = pokemon_factory(trainer=user)

    team = team_factory(
        name="My team",
        trainer=user,
        pokemon_1=pokemon_team[0],
        pokemon_2=pokemon_team[1],
        pokemon_3=pokemon_team[2],
    )

    playload = {
        "pokemon_1": pokemon_team[0].id,
        "pokemon_2": pokemon_team[1].id,
        "pokemon_3": pokemon_team[2].id,
        "pokemon_4": another_pokemon.id,
        "pokemon_5": "",
    }

    res = client_log.patch(
        reverse("teams:teams-detail", kwargs={"pk": team.id}),
        playload,
        format="json",
    )

    assert res.status_code == status.HTTP_200_OK
    team.refresh_from_db()
    assert team.pokemon_4 == another_pokemon

    pokemon_4 = Pokemon.objects.get(id=res.data.get("pokemon_4"))
    assert pokemon_4.team == team.name
    assert pokemon_4.team_pk == team.id


def test_full_update_team(team_factory, pokemon_factory, user_log, client_log):
    """Test updating a team by authenticated user"""
    user = user_log

    # First team
    pokemon_team_1 = [pokemon_factory(trainer=user_log) for i in range(5)]
    
    team = team_factory(
        name="My team",
        trainer=user,
        pokemon_1=pokemon_team_1[0],
        pokemon_2=pokemon_team_1[1],
        pokemon_3=pokemon_team_1[2],
        pokemon_4=pokemon_team_1[3],
        pokemon_5=pokemon_team_1[4]

    )

    # Second team witch remplace pokemon
    pokemon_team_2 = [pokemon_factory(trainer=user_log) for i in range(5)]

    playload = {
        "name": "My best team",
        "trainer": user.id,
        "pokemon_1": pokemon_team_2[0].id,
        "pokemon_2": pokemon_team_2[1].id,
        "pokemon_3": pokemon_team_2[2].id,
        "pokemon_4": pokemon_team_2[3].id,
        "pokemon_5": pokemon_team_2[4].id,
    }

    res = client_log.put(
        reverse("teams:teams-detail", kwargs={"pk": team.id}),
        playload,
        format="json",
    )

    assert res.status_code == status.HTTP_200_OK
    team.refresh_from_db()
    assert team.name == "My best team"
    for i in range(5):
      poke_field = "pokemon_{}".format(i+1)
      assert getattr(team, poke_field) == pokemon_team_2[i]


    for i in range(5):
        check_poke_field_1 = Pokemon.objects.get(id=pokemon_team_1[i].id)
        assert check_poke_field_1.team == None
        assert check_poke_field_1.team_pk == None

        check_poke_field_2 = Pokemon.objects.get(id=pokemon_team_2[i].id)
        assert check_poke_field_2.team == team.name
        assert check_poke_field_2.team_pk == team.id


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
    pokemon_team = [pokemon_factory(trainer=user_log) for i in range(5)]

    team = team_factory(
        name="My team",
        trainer=user_log,
        pokemon_1=pokemon_team[0],
        pokemon_2=pokemon_team[1],
        pokemon_3=pokemon_team[2],
        pokemon_4=pokemon_team[3],
        pokemon_5=pokemon_team[4],
    )

    res = client_log.delete(reverse("teams:teams-detail", kwargs={"pk": team.id}))
    assert res.status_code == status.HTTP_204_NO_CONTENT

    for i in range(5):
        pokemon = Pokemon.objects.get(id=pokemon_team[i].id)
        assert pokemon.team == None
        assert pokemon.team_pk == None
                                  
