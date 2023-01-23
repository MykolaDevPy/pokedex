from favorite_object.models import FavoriteObject


def get_random_object():
    """Get a random object from the database"""
    return FavoriteObject.objects.all().order_by("?").first()
