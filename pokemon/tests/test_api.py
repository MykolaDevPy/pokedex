import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Pokemon
from ..serializers import PokemonSerializer
from ..serializers import PokemonDetailsSerializer

pytestmark = pytest.mark.django_db


def test_listing_pokemons(user_log, client_log, client_admin, pokemon_factory):
    """Test listing Pokedex creatures."""

    # Create 3 pokemons
    pokemon_factory()
    pokemon_factory(trainer=user_log)
    pokemon_factory(trainer=user_log)
    pokemon_factory()

    # Unauthenticated user should be denied access
    res = APIClient().get(reverse("pokemon:pokemon-list"))
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

    # Authenticated user should be given access
    res = client_log.get(reverse("pokemon:pokemon-list"))
    assert res.status_code == status.HTTP_200_OK

    pokemons = Pokemon.objects.filter(trainer=user_log.id)
    serializer = PokemonSerializer(pokemons, many=True)

    assert res.status_code == status.HTTP_200_OK
    assert len(serializer.data) == 2
    assert serializer.data == res.data.get("results")

    # Super user should see all results
    res = client_admin.get(reverse("pokemon:pokemon-list"))
    assert res.status_code == status.HTTP_200_OK

    pokemons = Pokemon.objects.all()
    serializer = PokemonSerializer(pokemons, many=True)

    assert res.status_code == status.HTTP_200_OK
    assert len(serializer.data) == 4
    assert serializer.data == res.data.get("results")


def test_view_pokemon_detail(user_log, client_log, pokemon_factory):
    """Test retrieving a Pokemon creature"""

    # Create 2 pokemons
    pokemon_factory()
    pokemon = pokemon_factory(trainer=user_log)

    # Unauthenticated user should be denied access
    res = APIClient().get(reverse("pokemon:pokemon-detail", args=[pokemon.id]))
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

    # Authenticated user should be given access
    res = client_log.get(reverse("pokemon:pokemon-detail", args=[pokemon.id]))
    assert res.status_code == status.HTTP_200_OK

    serializer = PokemonDetailsSerializer(pokemon)

    assert res.status_code == status.HTTP_200_OK
    assert serializer.data == res.data


def test_create_pokemon(
    user_log,
    client_log,
    pokedex_creature_factory,
    pokemon_factory,
):
    """Authenticated user can create a pokermon"""
    creature = pokedex_creature_factory(name="Brown Bear")
    pokemon_factory()
    pokemon_factory()

    # Create a trained pokemon
    payload = {
        "pokedex_creature": creature.id,
        "trainer": user_log.id,
        "nickname": "Gozilla",
    }
    res = client_log.post(
        reverse("pokemon:pokemon-list"),
        payload,
        format="json",
    )
    assert res.status_code == status.HTTP_201_CREATED

    pokemon = Pokemon.objects.get(id=res.data["id"])
    assert str(pokemon) == "Gozilla (tai)"
    assert pokemon.pokedex_creature.name == "Brown Bear"

    # Create a wild pokemon
    payload = {
        "pokedex_creature": creature.id,
    }
    res = client_log.post(
        reverse("pokemon:pokemon-list"),
        payload,
        format="json",
    )
    assert res.status_code == status.HTTP_201_CREATED

    pokemon = Pokemon.objects.get(id=res.data["id"])
    assert str(pokemon) == "Brown Bear (wild)"


def test_partial_update_pokemon(user_log, client_log, pokemon_factory):
    """Authenticated user can update an existing pokemon with patch"""
    user = user_log
    
    pokemon = pokemon_factory(nickname="Lion", trainer=user,)
    
    payload = {"nickname": "Monster king"}
    
    res = client_log.patch(
        reverse("pokemon:pokemon-detail", kwargs={"pk": pokemon.id}),
        payload,
        format="json",
    )
    assert res.status_code == status.HTTP_200_OK
    
    pokemon.refresh_from_db()
    assert pokemon.nickname == payload["nickname"]


def test_full_update_pokemon(
    client_log, user_log, pokedex_creature_factory, pokemon_factory
):
    """Authenticated user can update an existing pokemon with put"""
    pokemon = pokemon_factory(trainer=user_log)
    creature = pokedex_creature_factory()
    payload = {
        "nickname": "Monster king",
        "pokedex_creature": creature.id,
    }
    res = client_log.put(
        reverse("pokemon:pokemon-detail", args=[pokemon.id]),
        payload,
        format="json",
    )
    assert res.status_code == status.HTTP_200_OK
    pokemon.refresh_from_db()
    assert pokemon.nickname == payload["nickname"]
    assert pokemon.trainer == user_log
    assert pokemon.pokedex_creature == creature


def test_delete_pokemon(user_log, client_log, client_admin, pokemon_factory):
    """Authenticated user can delete an existing pokermon"""
    pokemon_1 = pokemon_factory(trainer=user_log)
    pokemon_2 = pokemon_factory()
    
    # Regular users can delete only your own pokemons
    res = client_log.delete(reverse("pokemon:pokemon-detail", args=[pokemon_1.id]))
    assert res.status_code == status.HTTP_204_NO_CONTENT

    assert not Pokemon.objects.filter(id=pokemon_1.id).exists()

    res = client_log.delete(reverse("pokemon:pokemon-detail", args=[pokemon_2.id]))
    assert res.status_code == status.HTTP_404_NOT_FOUND

    # Superuser can delete anyone pokemon
    res = client_admin.delete(reverse("pokemon:pokemon-detail", args=[pokemon_2.id]))
    assert res.status_code == status.HTTP_204_NO_CONTENT

    assert not Pokemon.objects.filter(id=pokemon_2.id).exists()


def test_give_xp_to_pokemon(user_log, client_log, pokemon_factory):
    """Authenticated user can give XP to an existing pokermon"""
    pokemon = pokemon_factory(level=1, experience=40, trainer=user_log,)

    payload = {
        "amount": 150,
    }
    res = client_log.post(
        reverse("pokemon:pokemon-give-xp", args=[pokemon.id]),
        payload,
        format="json",
    )
    assert res.status_code == status.HTTP_200_OK

    pokemon = Pokemon.objects.get(id=pokemon.id)
    pokemon.refresh_from_db()

    assert pokemon.level == 2
    assert pokemon.experience == 190


def test_give_xp_to_pokemon_invalid_request(user_log, client_log, pokemon_factory):
    """Authenticated user can give XP to an existing pokermon"""
    pokemon = pokemon_factory(level=1, experience=40, trainer=user_log,)

    payload = {
        "amount": "Hello",
    }
    res = client_log.post(
        reverse("pokemon:pokemon-give-xp", args=[pokemon.id]),
        payload,
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    error_detail = res.data['amount'][0]
    error_message = str(error_detail)
    assert error_message == "A valid integer is required."

    payload = {
        "attack": 100,
    }
    res = client_log.post(
        reverse("pokemon:pokemon-give-xp", args=[pokemon.id]),
        payload,
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    error_detail = res.data['amount'][0]
    error_message = str(error_detail)
    assert error_message == "This field is required."
