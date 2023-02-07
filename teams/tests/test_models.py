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

    team_1 = team_factory(
        name=name,
        trainer=trainer,
    )

    pokemon_creature_1 = pokedex_creature_factory(name="Paras")
    pokemon_factory(pokedex_creature=pokemon_creature_1, team=team_1, trainer=trainer)
    pokemon_creatture_2 = pokedex_creature_factory(name="Ponyta")
    pokemon_factory(pokedex_creature=pokemon_creatture_2, team=team_1, trainer=trainer)

    assert str(team_1) == "Team 'Test Team' (by tai): Paras, Ponyta."




    
    