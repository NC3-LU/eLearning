from functools import wraps
from uuid import UUID

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.template import TemplateDoesNotExist
from django.utils.translation import gettext_lazy as _

from .models import User


def user_uuid_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_uuid = request.session.get("user_uuid", None)
        if user_uuid is None:
            messages.error(request, _("Session expired or browser sessions conflict"))
            request_path = request.path
            if (
                "update_progress_bar" in request_path
                or "change_slide" in request_path
                or "resources_download" in request_path
                or "report" in request_path
            ):
                return HttpResponseBadRequest()
            return HttpResponseRedirect("/")
        try:
            User.objects.get(uuid=UUID(user_uuid))
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return HttpResponseRedirect("/")
        except User.DoesNotExist:
            messages.error(request, _("User does not exist"))
            return HttpResponseRedirect("/")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def handle_template_not_found(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except TemplateDoesNotExist:
            raise Http404

    return wrapped_view


def stats_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if getattr(settings, "ALLOW_ANONYMOUS_STATS_ACCESS", False):
            return view_func(request, *args, **kwargs)
        else:
            return user_passes_test(
                lambda u: u.is_authenticated, login_url=settings.LOGIN_URL
            )(view_func)(request, *args, **kwargs)

    return _wrapped_view
