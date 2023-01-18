from django.contrib import admin

from .models import FavoriteObject


class FavoriteObjectAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in FavoriteObject._meta.fields if field.name != "id"
    ]
    ordering = ("name",)
    search_fields = ("name",)
    list_per_page = 30


admin.site.register(FavoriteObject, FavoriteObjectAdmin)
