from django.conf import settings
from django.db import models

from pokemon.models import Pokemon


class Team(models.Model):
    """Team model"""

    name = models.CharField(max_length=100)

    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    pokemon_1 = models.ForeignKey(
        Pokemon,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    pokemon_2 = models.ForeignKey(
        Pokemon,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    pokemon_3 = models.ForeignKey(
        Pokemon,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    pokemon_4 = models.ForeignKey(
        Pokemon,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    pokemon_5 = models.ForeignKey(
        Pokemon,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
