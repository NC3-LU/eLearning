from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from .settings import SITE_NAME


# Customize the admin site
class CustomAdminSite(admin.AdminSite):
    site_header = SITE_NAME + " " + _("Administration")
    site_title = SITE_NAME

    def admin_view(self, view, cacheable=False):
        # decorated_view = otp_required(view)
        decorated_view = login_required(view)
        return super().admin_view(decorated_view, cacheable)


admin_site = CustomAdminSite()
