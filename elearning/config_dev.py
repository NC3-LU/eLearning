import os

PUBLIC_URL = ""
ALLOWED_HOSTS = ["127.0.0.1", locals().get("PUBLIC_URL", "")]
HOST_CONTACT = {
    "name": "Organization Name",
    "street": "Organization Street",
    "zip_code": "Organization Zip Code",
    "country": "Organization Country",
    "phone": "Organization Phone Number",
    "website": "https://www.example.org",
    "contact_email": "contact@example.org",
    "privacy_email": "privacy@exemple.org",
    "tos_url": None,  # "https://www.example.org/tos"
    "privacy_policy_url": None,  # "https://www.example.org/privacy_policy"
    "contact_url": None,  # "https://www.example.org/contact_us"
}

# The generic site/tool name. Used to load specific config, templates, styles, logo.
SITE_NAME = "E-Learning Platform"

SECRET_KEY = "django-insecure-1*nt5exfgm+po13ngrz7fm5sitfvi24f!13t=z*l5zz*w9zic$"

HASH_KEY = b"#StandWithtUkraineHP-TmGv-4z7h-1xaQp0RYuY20="

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "db",
        "PORT": 5432,
    }
}

CORS_ALLOWED_ORIGINS = []
CORS_ALLOWED_ORIGIN_REGEXES = []
CORS_ALLOW_METHODS = [
    "GET",
    "OPTIONS",
]

EMAIL_HOST = "localhost"
EMAIL_PORT = 25

# Logging mechanism
LOG_DIRECTORY = "./logs"
LOG_FILE = "django.log"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "INFO", "handlers": ["file"]},
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIRECTORY, LOG_FILE),
            "formatter": "app",
        },
    },
    "loggers": {
        "django": {"handlers": ["file"], "level": "INFO", "propagate": True},
    },
    "formatters": {
        "app": {
            "format": (
                "%(asctime)s [%(levelname)-8s] (%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
}
