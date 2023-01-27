from rest_framework import serializers

from .models import Pokemon
from authentication.serializers import UserSerializer
from favorite_object.serializers import FavoriteObjectDetailSerializer
from pokedex.serializers import PokedexCreatureDetailSerializer


class PokemonSerializer(serializers.ModelSerializer):
    """Serializer of Pokemon object"""

    class Meta:
        model = Pokemon
        fields = (
            "id",
            "pokedex_creature",
            "trainer",
            "nickname",
            "level",
            "experience",
        )
        read_only_fields = (
            "id",
            "level",
        )

    def validate(self, attrs):
        """Add pokemon nickname if no nickname is given"""
        nickname = attrs.get("nickname")
        pokedex_creature = attrs.get("pokedex_creature")
        if not nickname:
            attrs["nickname"] = pokedex_creature.name

        return super().validate(attrs)


class PokemonDetailsSerializer(serializers.ModelSerializer):
    """Serializer of Pokemon details object"""

    pokedex_creature = PokedexCreatureDetailSerializer()
    trainer = UserSerializer()
    favorite_object = FavoriteObjectDetailSerializer()

    class Meta:
        model = Pokemon
        fields = (
            "id",
            "nickname",
            "level",
            "experience",
            "pokedex_creature",
            "trainer",
            "favorite_object",
            "team",
            "team_pk",
        )

        read_only_fields = (
            "id",
            "level",
            "team",
            "team_pk",
        )


class PokemonTeamDetailsSerializer(serializers.ModelSerializer):
    """Serializer of Pokemon details object"""

    pokedex_creature = PokedexCreatureDetailSerializer()
    favorite_object = FavoriteObjectDetailSerializer()

    class Meta:
        model = Pokemon
        fields = (
            "id",
            "nickname",
            "level",
            "experience",
            "pokedex_creature",
            "favorite_object",
        )

        read_only_fields = (
            "id",
            "level",
        )



class PokemonWildSerializer(serializers.ModelSerializer):
    """Serializer of wild pokemon endpoint"""

    pokedex_creature = PokedexCreatureDetailSerializer()
    favorite_object = FavoriteObjectDetailSerializer()

    class Meta:
        model = Pokemon
        fields = (
            "id",
            "level",
            "experience",
            "pokedex_creature",
            "favorite_object",
        )

        read_only_fields = (
            "id",
            "level",
        )


class PokemonGiveXPSerializer(serializers.Serializer):
    """Serializer of give-xp endpoint"""

    amount = serializers.IntegerField(min_value=0)
