from django.db.models.signals import post_delete
<<<<<<< HEAD
from django.db.models.signals import pre_init
=======
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
>>>>>>> 96f421481a0e9a7c783dd38b88ca71d8c3c593d2
from django.dispatch import receiver

from .models import Team
from pokemon.models import Pokemon


<<<<<<< HEAD
=======
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


>>>>>>> 96f421481a0e9a7c783dd38b88ca71d8c3c593d2
@receiver(post_save, sender=Team)
def assign_to_team(sender, instance, created, **kwargs):
    """Updating the information about team in Pokemon instance."""
    pokemons = []

<<<<<<< HEAD
    # Getting all pokemons assigned to this team
=======
>>>>>>> 96f421481a0e9a7c783dd38b88ca71d8c3c593d2
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
<<<<<<< HEAD
    
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
=======

    for pokemon in pokemons:
>>>>>>> 96f421481a0e9a7c783dd38b88ca71d8c3c593d2
        pokemon.team = instance
        pokemon.save()


@receiver(post_delete, sender=Team)
def remove_from_team(sender, instance, **kwargs):
    """Removing a team from Pokemon instance if Team instance is deleted."""
    pokemons = Pokemon.objects.filter(team=instance)
    for pokemon in pokemons:
        pokemon.team = None
        pokemon.save()
