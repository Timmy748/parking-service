from .settings import *

DEBUG = False

SECRET_KEY = (
    "django-insecure-_ik!%y7p#o^idk*ldfus$tg@-@^$-(6jy0lw-ww5l57%@-^bt-"
)

ALLOWED_HOSTS = ["127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "parking_service",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "parking_db",
        "PORT": "5432",
    }
}
