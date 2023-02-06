from rest_framework.serializers import SerializerMethodField
from rest_framework.serializers import ModelSerializer

import pokemon
from pokemon.serializers import PokemonTeamDetailsSerializer
from .models import Team
from authentication.serializers import UserSerializer



class TeamSerializer(ModelSerializer):
    """Serializer for Team instances"""

    class Meta:
        model = Team
        fields = (
            "id",
            "trainer",
            "name",
        )
        read_only_fields = ("id",)
    

class TeamDetailsSerializer(ModelSerializer):
    """Serializer for details of Team instances"""

    pokemons = SerializerMethodField()
    trainer = UserSerializer()

    class Meta:
        model = Team
        fields = (
            "id",
            "trainer",
            "name",
            "pokemons",
        )
        read_only_fields = ("id", "trainer",)


    def get_pokemons(self, obj):
        pokemons = pokemon.models.Pokemon.objects.filter(team=obj)
        return PokemonTeamDetailsSerializer(pokemons, many=True).data