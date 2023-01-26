from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .utils import *

from .models import Team
from pokemon.models import Pokemon


@receiver(pre_save, sender=Team)
def sort_pokemon(sender, instance, **kwargs) -> None:
    """Sort pokemons by None value and reassign the sorted pokemons to the corresponding fields"""
    pokemons = [
        instance.pokemon_1_id,
        instance.pokemon_2_id,
        instance.pokemon_3_id,
        instance.pokemon_4_id,
        instance.pokemon_5_id,
    ]

    pokemons.sort(key=lambda x: x == None)

    for i, pokemon_id in enumerate(pokemons):
        if pokemon_id:
            setattr(instance, f"pokemon_{i+1}", Pokemon.objects.get(id=pokemon_id))
        else:
            setattr(instance, f"pokemon_{i+1}", None)


@receiver(post_save, sender=Team)
def assign_to_team(sender, instance, created, **kwargs) -> None:
    """Updating the information about team in Pokemon instance."""
    pokemons = [
        instance.pokemon_1_id,
        instance.pokemon_2_id,
        instance.pokemon_3_id,
        instance.pokemon_4_id,
        instance.pokemon_5_id,
    ]
    
    # Remove the same pokemon from the  previous team
    if not created:
        set_changed_team(pokemons, instance)


    # Put the name of current Team in the Pokemon instance
    for pokemon_id in pokemons:
        if pokemon_id:
            pokemon = Pokemon.objects.get(pk=pokemon_id)
            pokemon.team = instance.name
            pokemon.save(update_fields=["team"])
            # Getting previous Teams where could be the same Pokemon
            check_another_teams(pokemon, instance)


@receiver(post_delete, sender=Team)
def remove_from_team(sender, instance, **kwargs) -> None:
    """Removing a team from Pokemon instance if Team instance is deleted."""
    pokemons = Pokemon.objects.filter(team=instance)
    for pokemon in pokemons:
        pokemon.team = None
        pokemon.save()
