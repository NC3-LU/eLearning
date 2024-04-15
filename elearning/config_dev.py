import os

from django.utils.translation import gettext_lazy as _

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

MEDIA_DIR = "theme/static/"

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

# Internationalization
# Django
LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ("en", "English"),
    ("fr", "Français"),
    ("de", "German"),
]

# Parler
PARLER_DEFAULT_LANGUAGE_CODE = "en"
PARLER_LANGUAGES = {
    1: (
        {
            "code": "fr",
        },  # French
        {
            "code": "en",
        },  # English
        {
            "code": "de",
        },  # German
    ),
    "default": {
        "fallbacks": ["en"],
        "hide_untranslated": False,
    },
}

# SESSION COOKIES
COOKIEBANNER = {
    "title": _("Cookie settings"),
    "groups": [
        {
            "id": "essential",
            "name": _("Essential"),
            "description": _(
                "This website uses cookies and other similar technologies strictly necessary \
                for its operation, without the use of personal data."
            ),
            "cookies": [
                {
                    "pattern": "cookiebanner",
                    "description": _("Meta cookie for the cookies that are set."),
                    "content": _("Accepted cookies"),
                    "max_age": _("6 months"),  # cookie_banner.js [max_age variable]
                },
                {
                    "pattern": "django_language",
                    "description": _("Meta cookie for user language settings"),
                    "content": _("Accepted cookies"),
                    "max_age": _("Session"),
                },
                {
                    "pattern": "csrftoken",
                    "description": _(
                        "This cookie prevents Cross-Site-Request-Forgery attacks."
                    ),
                    "content": _("Token"),
                    "max_age": _("6 months"),  # CSRF_COOKIE_AGE
                },
                {
                    "pattern": "sessionid",
                    "description": _("This cookie is necessary for user options"),
                    "content": _("session ID"),
                    "max_age": _("6 months"),  # SESSION_COOKIE_AGE
                },
            ],
        }
    ],
}

SESSION_COOKIE_AGE = 180 * 24 * 60 * 60  # 6 months, in seconds
CSRF_COOKIE_AGE = 180 * 24 * 60 * 60  # 6 months, in seconds
