##############################
# PARTIE SYSADMIN overriding
##############################
import django_env_overrides

DEBUG = False

STATIC_ROOT = "/var/www/static"
STATIC_URL = "/static/"

django_env_overrides.apply_to(globals())

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": PGHOST,
        "NAME": PGDATABASE,
        "USER": PGUSER,
        "PASSWORD": PGPASSWORD,
        "PORT": PGPORT,
    }
}
