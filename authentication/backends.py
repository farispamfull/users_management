from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


class AuthenticationBackend(BaseBackend):
    """
    Authentication Backend
    To manage the custom authentication process of user at email and password
    """

    def authenticate(self, **credentials):
        email = credentials.get('email', credentials.get('username'))
        try:
            user = User.objects.get(email=email)
            print(user)
        except User.DoesNotExist:
            return None
        if not user.check_password(credentials['password']):
            return None
        # if not user.is_verified:
        #     return None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
