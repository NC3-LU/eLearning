from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

from .managers import CustomUserManager

# sector
class Sector(TranslatableModel):
    translations = TranslatedFields(name=models.CharField(max_length=100))
    parent = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.CASCADE,
        blank=True,
        default=None,
        verbose_name=_("parent"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Sector")
        verbose_name_plural = _("Sectors")


# esssential services
class Services(TranslatableModel):
    translations = TranslatedFields(name=models.CharField(max_length=100))
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

# regulator and operator are companies
class Company(models.Model):
    is_regulator = models.BooleanField(default=False, verbose_name=_("Regulator"))
    identifier = models.CharField(
        max_length=64, verbose_name=_("Identifier")
    )  # requirement from business concat(name_country_regulator)
    name = models.CharField(max_length=64, verbose_name=_("name"))
    country = models.CharField(max_length=64, verbose_name=_("country"))
    address = models.CharField(max_length=255, verbose_name=_("address"))
    email = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default=None,
        verbose_name=_("email address"),
    )
    phone_number = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        default=None,
        verbose_name=_("phone number"),
    )
    sectors = models.ManyToManyField(Sector)
    monarc_path = models.CharField(max_length=200, verbose_name="MONARC URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")


# define an abstract class which make  the difference between operator and regulator
class User(AbstractUser):
    username = None
    is_staff = models.BooleanField(
        verbose_name=_("Administrator"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    phone_number = models.CharField(max_length=30, blank=True, default=None, null=True)
    companies = models.ManyToManyField(Company)
    sectors = models.ManyToManyField(Sector)
    email = models.EmailField(
        verbose_name=_("email address"),
        unique=True,
        error_messages={
            "unique": _("A user is already registered with this email address"),
        },
    )
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]



#incident
class Incident(models.Model):
    notification_date = models.DateField()

