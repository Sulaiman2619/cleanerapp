from functools import wraps
from django.http import HttpResponseForbidden

def is_cleaner(user):
    return hasattr(user, 'cleaner')

def is_staff(user):
    return hasattr(user, 'staff')

# Custom decorator to check if a user is a Cleaner
def cleaner_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if is_cleaner(request.user):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Permission Denied")
    return _wrapped_view

# Custom decorator to check if a user is a Staff
def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if is_staff(request.user):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Permission Denied")
    return _wrapped_view
