from functools import wraps

from django.http import HttpResponseRedirect

from .models import User


def user_uuid_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_uuid_param = request.GET.get("user_uuid", None)

        if user_uuid_param:
            request.session["user_uuid"] = user_uuid_param

        user_uuid = request.session.get("user_uuid", request.GET.get("user_uuid", None))
        if user_uuid is None:
            return HttpResponseRedirect("/")
        try:
            User.objects.get(uuid=user_uuid)
        except User.DoesNotExist:
            return HttpResponseRedirect("/")
        return view_func(request, *args, **kwargs)

    return _wrapped_view
