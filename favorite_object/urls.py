from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import FavoriteObjectViewSet

app_name = "favorite_object"

router = DefaultRouter()
router.register("", FavoriteObjectViewSet, basename="favorite-objects")

urlpatterns = [
    path("", include(router.urls)),
]
