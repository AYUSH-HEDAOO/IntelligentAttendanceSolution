from django.http import HttpResponse
from django.shortcuts import redirect
from core_apps.users.models import Role


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user and request.user.role_data.role_type in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect("Logout")

        return wrapper_func

    return decorator