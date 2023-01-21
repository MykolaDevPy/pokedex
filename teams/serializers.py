from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

import pokemon
from .models import Team
from authentication.serializers import UserSerializer


class TeamSerializer(ModelSerializer):
    """Serializer for Team instances"""

    class Meta:
        model = Team
        fields = (
            "trainer",
            "name",
            "pokemon_1",
            "pokemon_2",
            "pokemon_3",
            "pokemon_4",
            "pokemon_5",
        )
        read_only_fields = ("id")
        extra_kwargs = {
            "pokemon_1": {"allow_null": True, "required": False,},
            "pokemon_2": {"allow_null": True, "required": False,},
            "pokemon_3": {"allow_null": True, "required": False,},
            "pokemon_4": {"allow_null": True, "required": False,},
            "pokemon_5": {"allow_null": True, "required": False,},
        }
    

class TeamDetailsSerializer(ModelSerializer):
    """Serializer for details of Team instances"""

    pokemon_1 = SerializerMethodField()
    pokemon_2 = SerializerMethodField()
    pokemon_3 = SerializerMethodField()
    pokemon_4 = SerializerMethodField()
    pokemon_5 = SerializerMethodField()
    trainer = UserSerializer()

    class Meta:
        model = Team
        fields = (
            "trainer",
            "name",
            "pokemon_1",
            "pokemon_2",
            "pokemon_3",
            "pokemon_4",
            "pokemon_5",
        )
        read_only_fields = ("id",)

    # Methods to relate each Pokemon object
    def get_pokemon_1(self, obj):
        pokemon_1 = obj.pokemon_1
        if not pokemon_1:
            return None
        serializer = pokemon.serializers.PokemonDetailsSerializer(pokemon_1)
        return serializer.data
    
    def get_pokemon_2(self, obj):
        pokemon_2 = obj.pokemon_2
        if not pokemon_2:
            return None
        serializer = pokemon.serializers.PokemonDetailsSerializer(pokemon_2)
        return serializer.data
    
    def get_pokemon_3(self, obj):
        pokemon_3 = obj.pokemon_3
        if not pokemon_3:
            return None
        serializer = pokemon.serializers.PokemonDetailsSerializer(pokemon_3)
        return serializer.data
    
    def get_pokemon_4(self, obj):
        pokemon_4 = obj.pokemon_4
        if not pokemon_4:
            return None
        serializer = pokemon.serializers.PokemonDetailsSerializer(pokemon_4)
        return serializer.data
    
    def get_pokemon_5(self, obj):
        pokemon_5 = obj.pokemon_5
        if not pokemon_5:
            return None
        serializer = pokemon.serializers.PokemonDetailsSerializer(pokemon_5)
        return serializer.data
