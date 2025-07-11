from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        lookup = (
            {'email__iexact': username}
            if '@' in username else
            {User.USERNAME_FIELD + '__iexact': username}
        )
        try:
            user = User.objects.get(**lookup)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
