import logging
from uuid import UUID

from django.contrib import messages
from django.http import HttpRequest, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from .models import Level, User

# Get an instance of a logger
logger = logging.getLogger(__name__)


def find_user_by_uuid(user_uuid: UUID) -> User:
    """Get a user by its UUID."""
    try:
        return User.objects.get(uuid=user_uuid)
    except User.DoesNotExist as e:
        logger.error("User does not exist.")
        raise e


def set_next_level_user(request: HttpRequest, user: User) -> None:
    current_index = user.current_level.index
    next_level = Level.objects.filter(index__gt=current_index).order_by("index").first()

    if next_level:
        user.current_level = next_level
        first_level_position = user.current_level.get_first_level_position()
        if first_level_position:
            user.current_position = first_level_position
        else:
            user.current_position = None
        user.save()
    else:
        messages.success(
            request,
            _("Congratulations! You have completed all available levels.!"),
        )
        return HttpResponseRedirect("/dashboard")
