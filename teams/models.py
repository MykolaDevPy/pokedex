from django.conf import settings
from django.db import models

import pokemon


class Team(models.Model):
    """Team model"""

    name = models.CharField(max_length=100)

    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    

    def __str__(self):
        pokemons = pokemon.models.Pokemon.objects.filter(team=self.id)

        output_str = ", ".join([str(pokemon.nickname) for pokemon in pokemons]) + "."

        return "Team '{}' (by {}): {}".format(
            self.name,
            self.trainer,
            output_str,
        )

    

