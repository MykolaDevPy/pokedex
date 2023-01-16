from django.db import models

from pokemon.models import Pokemon

class FavoriteObject(models.Model):
  name = models.CharField(
      max_length=30,
      blank=False,
      null=False,
      unique=True
  )

  img_url = models.URLField(
    empty_value=False,
  )

  description = models.TextField(
    max_length=250,
    blank=False,
    null=False,
  )