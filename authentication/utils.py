from django.conf import settings
from django.contrib.auth import user_logged_out, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.timezone import now
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
    user.last_login = now()
    user.save()
    return token


def encode_uid(user_id):
    return force_str(urlsafe_base64_encode(force_bytes(user_id)))


def decode_uid(user_id):
    return force_str(urlsafe_base64_decode(user_id))


def send_token_for_email(request, user):
    uid = encode_uid(user.id)
    token = default_token_generator.make_token(user)
    current_site = get_current_site(request).domain
    relative_link = 'auth/email-verify'
    absurl = f'http://{current_site}/{relative_link}/{uid}/{token}'
    mail_subject = f'Verify your email from {current_site}'
    send_mail(mail_subject,
              f'Your verify link: {absurl}',
              f'{settings.EMAIL_FROM}@{current_site}',
              [user.email],
              fail_silently=False,
              )


def send_reset_password_for_email(request, user):
    uid = encode_uid(user.id)
    token = default_token_generator.make_token(user)
    current_site = get_current_site(request).domain
    relative_link = 'auth/reset-password/confirm/'
    absurl = f'http://{current_site}/{relative_link}/{uid}/{token}'
    mail_subject = f'reset password link from {current_site}'
    send_mail(mail_subject,
              f'Your reset password link: {absurl}',
              f'{settings.EMAIL_FROM}@{current_site}',
              [user.email],
              fail_silently=False,
              )
