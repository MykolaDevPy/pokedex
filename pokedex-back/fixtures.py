import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user_log(user_factory):
    """Return an user"""

    return user_factory(username="tai")


@pytest.fixture
def client_log(user_log):
    """Create an user and login"""

    client_log = APIClient()
    client_log.force_authenticate(user_log)

    return client_log


@pytest.fixture
def user_admin(user_factory):
    """Return a super user"""

    user = User.objects.create_superuser(username="admin", password="password")

    return user


@pytest.fixture
def client_admin(user_admin):
    """Create a super user and login"""

    client_log = APIClient()
    client_log.force_authenticate(user_admin)

    return client_log

