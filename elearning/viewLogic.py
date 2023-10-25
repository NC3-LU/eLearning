import logging
from uuid import UUID

from .models import User

# Get an instance of a logger
logger = logging.getLogger(__name__)


def find_user_by_uuid(user_uuid: UUID) -> User:
    """Get a user by its UUID."""
    try:
        return User.objects.get(uuid=user_uuid)
    except User.DoesNotExist as e:
        logger.error("User does not exist.")
        raise e
