from random import random

from rest_framework import serializers

from .models import Pokemon
from authentication.serializers import UserSerializer
from favorite_object.models import FavoriteObject
from favorite_object.serializers import FavoriteObjectSerializer
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
        """Add pokemon nickname if no nickname is given and add favorite object"""
        nickname = attrs.get("nickname")
        pokedex_creature = attrs.get("pokedex_creature")
        if not nickname:
            attrs["nickname"] = pokedex_creature.name

        #
        fav_object = FavoriteObject.objects.all()
        attrs["favorite_object"] = random.choice(fav_object)

        return super().validate(attrs)


class PokemonDetailsSerializer(serializers.ModelSerializer):
    pokedex_creature = PokedexCreatureDetailSerializer()
    trainer = UserSerializer()
    # favorite_object added
    favorite_object = FavoriteObjectSerializer()

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
        )


class PokemonGiveXPSerializer(serializers.Serializer):
    """Serializer of give-xp endpoint"""

    amount = serializers.IntegerField(min_value=0)
