from .settings import *

DEBUG = True

SECRET_KEY = (
    "django-insecure-_ik!%y7p#o^idk*ldfus$tg@-@^$-(6jy0lw-ww5l57%@-^bt-"
)

ALLOWED_HOSTS = ["127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
