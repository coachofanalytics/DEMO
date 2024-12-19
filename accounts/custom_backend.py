from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authenticate using either username or email.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        try:
            # Determine if the username is an email or a username
            user = User.objects.get(
                **({'email': username} if '@' in username else {'username': username})
            )
        except User.DoesNotExist:
            return None
        # Validate the password and return the user if valid
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
