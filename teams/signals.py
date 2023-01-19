from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Team
from pokemon.models import Pokemon


@receiver(pre_save, sender=Team)
def verify_ownership(sender, instance, **kwargs):
    """Verify ownership of a given instance before saving."""

    try:
        pokemon = Pokemon.objects.get(pk=instance.pokemon_1_id)
        if pokemon.trainer == instance.trainer:
            instance.pokemon_1 = pokemon
        else:
            instance.pokemon_1 = None
    except Pokemon.DoesNotExist:
        instance.pokemon_1 = None

    if instance.pokemon_2_id:
        try:
            pokemon = Pokemon.objects.get(pk=instance.pokemon_2_id)
            if pokemon.trainer == instance.trainer:
                instance.pokemon_2 = pokemon
            else:
                instance.pokemon_2 = None
        except Pokemon.DoesNotExist:
            instance.pokemon_2 = None

    if instance.pokemon_3_id:
        try:
            pokemon = Pokemon.objects.get(pk=instance.pokemon_3_id)
            if pokemon.trainer == instance.trainer:
                instance.pokemon_3 = pokemon
            else:
                instance.pokemon_3 = None
        except Pokemon.DoesNotExist:
            instance.pokemon_3 = None
    
    if instance.pokemon_4_id:
        try:
            pokemon = Pokemon.objects.get(pk=instance.pokemon_4_id)
            if pokemon.trainer == instance.trainer:
                instance.pokemon_4 = pokemon
            else:
                instance.pokemon_4 = None
        except Pokemon.DoesNotExist:
            instance.pokemon_4 = None
    
    if instance.pokemon_5_id:
        try:
            pokemon = Pokemon.objects.get(pk=instance.pokemon_5_id)
            if pokemon.trainer == instance.trainer:
                instance.pokemon_5 = pokemon
            else:
                instance.pokemon_5 = None
        except Pokemon.DoesNotExist:
            instance.pokemon_5 = None


@receiver(post_save, sender=Team)
def assign_to_team(sender, instance, created, **kwargs):
    """Updating the information about team in Pokemon instance."""

    if created:
        pokemons = []

        for i in range(1,6):
            poke_field = 'pokemon_' + str(i)
            if getattr(instance, poke_field):
                pokemons.append(Pokemon.objects.get(pk=getattr(instance, poke_field).id))

        for pokemon in pokemons:
            pokemon.team = instance
            pokemon.save()

    if not created:
        pokemons = []
        prev_pokemons = Pokemon.objects.filter(team=instance)

        for i in range(1,6):
            poke_field = 'pokemon_' + str(i)
            if getattr(instance, poke_field):
                pokemons.append(Pokemon.objects.get(pk=getattr(instance, poke_field).id))
        
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


