from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Team(models.Model):
    """Team model"""

    name = models.CharField(max_length=100)

    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    pokemon_1 = models.ForeignKey(
        "pokemon.Pokemon",
        on_delete=models.SET_NULL,
        null=True,
        related_name='pokemon_1_team',
    )

    pokemon_2 = models.ForeignKey(
        "pokemon.Pokemon",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='pokemon_2_team',
    )

    pokemon_3 = models.ForeignKey(
        "pokemon.Pokemon",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='pokemon_3_team',
    )

    pokemon_4 = models.ForeignKey(
        "pokemon.Pokemon",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='pokemon_4_team',
    )

    pokemon_5 = models.ForeignKey(
        "pokemon.Pokemon",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='pokemon_5_team',
    )
    

    def __str__(self):
        pokemons = [self.pokemon_1, self.pokemon_2, self.pokemon_3, self.pokemon_4, self.pokemon_5]

        output_str = ", ".join([str(pokemon.nickname) for pokemon in pokemons if pokemon]) + "."

        return "Team '{}' (by {}): {}".format(
            self.name,
            self.trainer,
            output_str,
        )

    

