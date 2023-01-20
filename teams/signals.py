from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Team
from pokemon.models import Pokemon


@receiver(pre_save, sender=Team)
def verify_ownership(sender, instance, **kwargs):
    """Verify ownership of a given instance before saving."""
    pokemons = [
        instance.pokemon_1_id,
        instance.pokemon_2_id,
        instance.pokemon_3_id,
        instance.pokemon_4_id,
        instance.pokemon_5_id,
    ]

    pokemons.sort(key=lambda x: x != None)

    for i, pokemon in enumerate(pokemons):
        setattr(instance, f"pokemon_{i+1}", pokemon)


@receiver(post_save, sender=Team)
def assign_to_team(sender, instance, created, **kwargs):
    """Updating the information about team in Pokemon instance."""
    pokemons = []

    for i in range(1, 6):
        poke_field = "pokemon_" + str(i)
        if getattr(instance, poke_field):
            pokemons.append(Pokemon.objects.get(pk=getattr(instance, poke_field).id))

    if not created:
        prev_pokemons = Pokemon.objects.filter(team=instance)

        for prev_pokemon in prev_pokemons:
            if prev_pokemon not in pokemons:
                prev_pokemon.team = None
                prev_pokemon.save()

    for pokemon in pokemons:
        pokemon.team = instance
        pokemon.save()


@receiver(post_delete, sender=Team)
def remove_from_team(sender, instance, **kwargs):
    """Removing a team from Pokemon instance if Team instance is deleted."""
    pokemons = Pokemon.objects.filter(team=instance)
    for pokemon in pokemons:
        pokemon.team = None
        pokemon.save()
