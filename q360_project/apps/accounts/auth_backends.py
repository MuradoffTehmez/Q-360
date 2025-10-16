"""
Custom authentication backends for Q360.
Allows users to login with email or username.
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend that allows login with email or username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user with email or username.
        """
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)

        if username is None or password is None:
            return None

        try:
            # Try to find user by username or email (case insensitive)
            user = User.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except User.DoesNotExist:
            # User not found
            return None
        except User.MultipleObjectsReturned:
            # Multiple users with same email - use username only
            try:
                user = User.objects.get(username__iexact=username)
            except User.DoesNotExist:
                return None

        # Check password
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None

    def user_can_authenticate(self, user):
        """
        Check if user is active and can authenticate.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None