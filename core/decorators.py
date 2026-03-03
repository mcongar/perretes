from functools import wraps
from django.shortcuts import redirect


def redirect_if_authenticated(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('perfil', username=request.user.username)
        return view_func(request, *args, **kwargs)
    return wrapper