# Generated by Django 3.2.12 on 2023-01-23 17:43

from django.db import migrations, models
import django.db.models.deletion
import pokemon.utils


class Migration(migrations.Migration):

    dependencies = [
        ('favorite_object', '0003_alter_favoriteobject_img_url'),
        ('pokemon', '0002_rename_surname_pokemon_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='favorite_object',
            field=models.ForeignKey(default=pokemon.utils.get_random_object, null=True, on_delete=django.db.models.deletion.SET_NULL, to='favorite_object.favoriteobject'),
        ),
    ]
