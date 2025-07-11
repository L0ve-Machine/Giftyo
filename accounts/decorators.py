# accounts/decorators.py

from functools import wraps
from django.contrib.auth import logout

def public_view(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return view_func(request, *args, **kwargs)
    return _wrapped
