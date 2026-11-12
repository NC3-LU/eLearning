import os
import sys

from elearning.config_dev import *  # noqa: F403

DEBUG = False
PUBLIC_URL = os.getenv("PUBLIC_URL", "")
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,web").split(",")
    if host.strip()
]

SECRET_KEY = os.getenv("SECRET_KEY", SECRET_KEY)  # noqa: F405
HASH_KEY = os.getenv("HASH_KEY", HASH_KEY.decode()).encode()  # noqa: F405

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "postgres"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "password"),
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "PORT": int(os.getenv("POSTGRES_PORT", "5432")),
    }
}

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
COOKIEBANNER_SECURE = not DEBUG

LOG_DIRECTORY = ""
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "INFO", "handlers": ["console"]},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "app",
        }
    },
    "formatters": {
        "app": {
            "format": "%(asctime)s [%(levelname)-8s] (%(module)s.%(funcName)s) %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
}
