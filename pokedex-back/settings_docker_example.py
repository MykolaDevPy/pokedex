##############################
# PARTIE SYSADMIN overriding
##############################
import django_env_overrides
import os

DEBUG = False

STATIC_ROOT = "/var/www/static"
STATIC_URL = "/static/"

django_env_overrides.apply_to(globals())

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("PGHOST"),
        "NAME": os.getenv("PGDATABASE"),
        "USER": os.getenv("PGUSER"),
        "PASSWORD": os.getenv("PGPASSWORD"),
        "PORT": os.getenv("PGPORT"),
    }
}
