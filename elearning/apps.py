from django.apps import AppConfig

from .settings import SITE_NAME


class ElearningConfig(AppConfig):
    name = "elearning"
    verbose_name = SITE_NAME
