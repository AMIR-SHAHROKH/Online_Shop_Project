from django.contrib.auth import get_user_model
from .models import User
from django.contrib.auth.backends import BaseBackend

def custom_authenticate(request, username=None, password=None):
    if username is None or password is None:
        return None

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # No user was found, return None
        return None

    # Check if the password is correct
    if user.check_password(password):
        return user
    else:
        return None
