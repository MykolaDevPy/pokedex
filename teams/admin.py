from django.contrib import admin

from .models import Team

class TeamAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Team._meta.fields if field.name != "id"]
    search_fields = ("name", "trainer__username",)
    ordering = ("name",)
    list_per_page = 30

    autocomplete_fields = ("trainer", "pokemon_1", "pokemon_2", "pokemon_3", "pokemon_4", "pokemon_5",)

admin.site.register(Team, TeamAdmin)