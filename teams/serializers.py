from rest_framework.serializers import ModelSerializer

from .models import Team
from authentication.serializers import UserSerializer


class TeamSerializer(ModelSerializer):
    """Serializer for Team instances"""

    class Meta:
        model = Team
        fields = "__all__"
        read_only_fields = ("id", "trainer")
        extra_kwargs = {
            "pokemon_1": {"allow_null": True, "required": False,},
            "pokemon_2": {"allow_null": True, "required": False,},
            "pokemon_3": {"allow_null": True, "required": False,},
            "pokemon_4": {"allow_null": True, "required": False,},
            "pokemon_5": {"allow_null": True, "required": False,},
        }
    

class TeamDetailsSerializer(ModelSerializer):
    """Serializer for details of Team instances"""

    pokemon_details_serialezer = "pokemon.serializers.PokemonDetailsSerializer"

    pokemon_1 = pokemon_details_serialezer
    pokemon_2 = pokemon_details_serialezer
    pokemon_3 = pokemon_details_serialezer
    pokemon_4 = pokemon_details_serialezer
    pokemon_5 = pokemon_details_serialezer
    trainer = UserSerializer()

    class Meta:
        model = Team
        fields = "__all__"
        read_only_fields = ("id", "trainer", "pokemon_1", "pokemon_2", "pokemon_3", "pokemon_4", "pokemon_5")
