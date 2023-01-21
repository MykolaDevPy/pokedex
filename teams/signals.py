from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.db.models.signals import pre_init
from django.dispatch import receiver

from .models import Team
from pokemon.models import Pokemon


@receiver(post_save, sender=Team)
def assign_to_team(sender, instance, created, **kwargs):
    """Updating the information about team in Pokemon instance."""
    pokemons = []

    # Getting all pokemons assigned to this team
    for i in range(1, 6):
        poke_field = "pokemon_" + str(i)
        if getattr(instance, poke_field):
            pokemons.append(Pokemon.objects.get(pk=getattr(instance, poke_field).id))

    # Executed only if update of DB
    if not created:
        prev_pokemons = Pokemon.objects.filter(team=instance)

        for prev_pokemon in prev_pokemons:
            if prev_pokemon not in pokemons:
                prev_pokemon.team = None
                prev_pokemon.save()
    
    # Put the name of current Team in the Pokemon instance
    for pokemon in pokemons:
        # Getting previous Teams where could be the same Pokemon
        another_team = Team.objects.filter(
            Q(pokemon_1=pokemon) | 
            Q(pokemon_2=pokemon) | 
            Q(pokemon_3=pokemon) | 
            Q(pokemon_4=pokemon) | 
            Q(pokemon_5=pokemon)
        ).first()
        if another_team:
            for i in range(1, 6):
                poke_field = "pokemon_%d" % i
                # Delete current pokemon from previous team
                if getattr(another_team, poke_field ) == pokemon:
                    setattr(another_team, poke_field, None)
                    another_team.save()
        pokemon.team = instance
        pokemon.save()


@receiver(post_delete, sender=Team)
def remove_from_team(sender, instance, **kwargs):
    """Removing a team from Pokemon instance if Team instance is deleted."""
    pokemons = Pokemon.objects.filter(team=instance)
    for pokemon in pokemons:
        pokemon.team = None
        pokemon.save()


