import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from favorite_object.models import FavoriteObject
from favorite_object.serializers import FavoriteObjectSerializer
from favorite_object.serializers import FavoriteObjectDetailSerializer

pytestmark = pytest.mark.django_db

def test_listing_favorite_object(favorite_object_factory, client_log):
  """Test listing of favorite objects"""

  # Create 3 objects
  favorite_object_factory()
  favorite_object_factory()
  favorite_object_factory()

  # Unauthenticated users should be denied access
  res = APIClient().get(reverse("favorite_object:favorite-object-list"))

  assert res.status_code == status.HTTP_401_UNAUTHORIZED

  # Authenticated users should be allowed access
  res = client_log.get(reverse("favorite_object:favorite-object-list"))
  fav_objects = FavoriteObject.objects.all()
  serializer = FavoriteObjectSerializer(fav_objects, many=True)

  assert res.status_code == status.HTTP_200_OK
  assert len(fav_objects) == 3
  assert serializer.data == res.data["results"]

def test_view_favorite_object_detail(favorite_object_factory, client_log):
  """Test retrieving a Favorite object."""

  # Create 3 objects
  favorite_object_factory()
  favorite_object_factory()
  fav_object = favorite_object_factory()

  # Unauthenticated users should be denied access
  res = APIClient().get(reverse("favorite_object:favorite-object-detail", args=[fav_object.id]))

  assert res.status_code == status.HTTP_401_UNAUTHORIZED

  # Authenticated users should be allowed access
  res = client_log.get(reverse("favorite_object:favorite-object-detail", args=[fav_object.id]))
  serializer = FavoriteObjectDetailSerializer(fav_object)

  assert res.status_code == status.HTTP_200_OK
  assert serializer.data == res.data

def test_filter_favorite_object_by_name(favorite_object_factory, client_log):
  """Test filtering Favorite object by name."""

  # Create 3 objects
  fav_object_1 = favorite_object_factory()
  fav_object_2 = favorite_object_factory()
  fav_object_3 = favorite_object_factory(name="My favorite object")

  # Unauthenticated users should be denied access
  res = APIClient().get(
    reverse("favorite_object:favorite-object-list"),
    {"name": "my fav"},
  )

  assert res.status_code == status.HTTP_401_UNAUTHORIZED

  # Authenticated users should be allowed access
  res = client_log.get(
    reverse("favorite_object:favorite-object-list"),
    {"name": "my fav"},
  )
  serializer_1 = FavoriteObjectSerializer(fav_object_1)
  serializer_2 = FavoriteObjectSerializer(fav_object_2)
  serializer_3 = FavoriteObjectSerializer(fav_object_3)

  assert res.status_code == status.HTTP_200_OK
  assert serializer_1.data not in res.data["results"]
  assert serializer_2.data not in res.data["results"]
  assert serializer_3.data in res.data["results"]



