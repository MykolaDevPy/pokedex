import pytest

pytestmark = pytest.mark.django_db


def test_teams_str(
        team_factory,
        pokedex_creature_factory,
        pokemon_factory,
        user_log
    ) -> None:
    """Test the __str__ method of Team instance."""

    name = "Test Team"
    trainer = user_log
    pokemon_creature_1 = pokedex_creature_factory(name="Paras")
    pokemon_1 = pokemon_factory(pokedex_creature=pokemon_creature_1)
    pokemon_creatture_2 = pokedex_creature_factory(name="Ponyta")
    pokemon_2 = pokemon_factory(pokedex_creature=pokemon_creatture_2)

    team_1 = team_factory(
        name=name,
        trainer=trainer,
        pokemon_1=pokemon_1,
        pokemon_2=pokemon_2,
        pokemon_3=None,
        pokemon_4=None,
        pokemon_5=None,
    )

    assert str(team_1) == "Team 'Test Team' (by tai): Pokemon 1, Pokemon 2."
    



    
    