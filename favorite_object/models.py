from django.db import models


class FavoriteObject(models.Model):
    name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
    )

    img_url = models.URLField()

    description = models.TextField(
        max_length=250,
        blank=False,
        null=False,
    )
