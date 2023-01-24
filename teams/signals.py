from django.db.models import Q
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Team
from pokemon.models import Pokemon


@receiver(pre_save, sender=Team)
def sort_pokemon(sender, instance, **kwargs):
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
def assign_to_team(sender, instance, created, **kwargs):
    """Updating the information about team in Pokemon instance."""
    pokemons = [
        instance.pokemon_1_id,
        instance.pokemon_2_id,
        instance.pokemon_3_id,
        instance.pokemon_4_id,
        instance.pokemon_5_id,
    ]

    prev_pokemons = Pokemon.objects.filter(team=instance)
    if prev_pokemons:
        for prev_pokemon in prev_pokemons:
            if prev_pokemon not in pokemons:
                prev_pokemon.team = None
                prev_pokemon.save()

    # Put the name of current Team in the Pokemon instance
    for pokemon_id in pokemons:
        if pokemon_id:
            pokemon = Pokemon.objects.get(pk=pokemon_id)
            pokemon.team = instance.name
            pokemon.save(update_fields=["team"])
            # Getting previous Teams where could be the same Pokemon
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


@receiver(post_delete, sender=Team)
def remove_from_team(sender, instance, **kwargs):
    """Removing a team from Pokemon instance if Team instance is deleted."""
    pokemons = Pokemon.objects.filter(team=instance)
    for pokemon in pokemons:
        pokemon.team = None
        pokemon.save()
