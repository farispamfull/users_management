from django.contrib.auth import user_logged_out, logout
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.authtoken.models import Token


def logout_user(request):
    request.user.auth_token.delete()
    user_logged_out.send(
        sender=request.user.__class__, request=request, user=request.user
    )
    logout(request)


def login_user(request, user):
    token, _ = Token.objects.get_or_create(user=user)
    user_logged_out.send(
        sender=request.user.__class__, request=request, user=request.user
    )
    return token


def encode_uid(user_id):
    return force_str(urlsafe_base64_encode(force_bytes(user_id)))


def decode_uid(user_id):
    return force_str(urlsafe_base64_decode(user_id))
