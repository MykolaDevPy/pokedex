# Generated by Django 3.2.12 on 2023-02-05 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='pokemon_1',
        ),
        migrations.RemoveField(
            model_name='team',
            name='pokemon_2',
        ),
        migrations.RemoveField(
            model_name='team',
            name='pokemon_3',
        ),
        migrations.RemoveField(
            model_name='team',
            name='pokemon_4',
        ),
        migrations.RemoveField(
            model_name='team',
            name='pokemon_5',
        ),
    ]
