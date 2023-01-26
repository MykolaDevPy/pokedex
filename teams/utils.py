from django.db.models import Q

from pokemon.models import Pokemon
from teams.models import Team



def set_changed_team(pokemons, instance) -> None:
    """
    Get all the pokemons of the given team and
    set None as value for pokemon if he is not more in this team.
    """
    
    prev_pokemons = Pokemon.objects.filter(team_id=instance.id)
    if prev_pokemons:
        for prev_pokemon in prev_pokemons:
            if prev_pokemon not in pokemons:
                prev_pokemon.team = None
                prev_pokemon.team_id = None
                prev_pokemon.save()

def check_another_teams(pokemon, instance) -> None:
    """
    Check if the given pokemon is already in another team and 
    remove it from previous team if it is.
    """
    another_team = Team.objects.filter(
                Q(pokemon_1=pokemon)
                | Q(pokemon_2=pokemon)
                | Q(pokemon_3=pokemon)
                | Q(pokemon_4=pokemon)
                | Q(pokemon_5=pokemon)
            ).exclude(pk=instance.id).first()
    if another_team:
        for i in range(1, 6):
            poke_field = "pokemon_%d" % i
            # Delete current pokemon from previous team
            if getattr(another_team, poke_field) == pokemon:
                setattr(another_team, poke_field, None)
                another_team.save(update_fields=[poke_field])