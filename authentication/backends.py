from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework.authentication import BaseAuthentication

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    """
    Authentication Backend
    To manage the custom authentication process of
    user at email and password, and is_verified status
    """

    def authenticate(self, request, **credentials):

        email = credentials.get(UserModel.USERNAME_FIELD,
                                credentials.get('username'))

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            UserModel().set_password(credentials['password'])
        else:

            if not user.check_password(credentials['password']):
                return None
            if not (user.is_staff or user.is_verified):
                return None

            return user



