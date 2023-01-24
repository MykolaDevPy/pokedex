from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField


import pokemon
from .models import Team
from authentication.serializers import UserSerializer
from pokemon.serializers import PokemonTeamDetailsSerializer


class TeamSerializer(ModelSerializer):
    """Serializer for Team instances"""

    class Meta:
        model = Team
        fields = (
            "id",
            "trainer",
            "name",
            "pokemon_1",
            "pokemon_2",
            "pokemon_3",
            "pokemon_4",
            "pokemon_5",
        )
        read_only_fields = ("id",)
        extra_kwargs = {
            "pokemon_1": {"allow_null": True, "required": False,},
            "pokemon_2": {"allow_null": True, "required": False,},
            "pokemon_3": {"allow_null": True, "required": False,},
            "pokemon_4": {"allow_null": True, "required": False,},
            "pokemon_5": {"allow_null": True, "required": False,},
        }

    
    def validate(self, obj):
            """Validation of Pokemon's owner."""
            for i in range(1, 6):
                poke_field = f"pokemon_{i}"
                if obj[poke_field]:
                    if obj[poke_field].trainer != self.context["request"].user:
                        obj[poke_field] = None
            
            return super().validate(obj)
    
    def create(self, validated_data):
        """Create a new Team instance"""
        return Team.objects.create(**validated_data)
    

class TeamDetailsSerializer(ModelSerializer):
    """Serializer for details of Team instances"""

    pokemon_1 = PokemonTeamDetailsSerializer()
    pokemon_2 = PokemonTeamDetailsSerializer()
    pokemon_3 = PokemonTeamDetailsSerializer()
    pokemon_4 = PokemonTeamDetailsSerializer()
    pokemon_5 = PokemonTeamDetailsSerializer()
    trainer = UserSerializer()

    class Meta:
        model = Team
        fields = (
            "id",
            "trainer",
            "name",
            "pokemon_1",
            "pokemon_2",
            "pokemon_3",
            "pokemon_4",
            "pokemon_5",
        )
        read_only_fields = ("id", "trainer",)
