from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

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

            if (user.check_password(credentials['password']) and
                    self.user_can_authenticate(user)):
                return user

    def user_can_authenticate(self, user):

        is_active = getattr(user, 'is_active', None)
        is_verified = getattr(user, 'is_verified', None)
        staff = user.is_staff
        return (is_active or is_active is None) and (staff or is_verified)
