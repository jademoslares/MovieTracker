from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from functools import wraps

def user_type_required(user_type):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.session.get('user_type') == user_type:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have access to this page.")
        return _wrapped_view
    return decorator