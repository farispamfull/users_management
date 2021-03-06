from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


def create_users_api(user_client):
    data = {
        'username': 'TestUser1234',
        'role': 'user',
        'email': 'testuser@gmail.fake',
    }
    user_client.post('/api/v1/users/', data=data)
    user = get_user_model().objects.get(email=data['email'])
    data = {
        'first_name': 'fsdfsdf',
        'last_name': 'dsgdsfg',
        'username': 'TestUser4321',
        'bio': 'Jdlkjd',
        'role': 'moderator',
        'email': 'testuser2342@gmail.fake',
        'is_verified': 'True',
    }
    user_client.post('/api/v1/users/', data=data)
    moderator = get_user_model().objects.get(username=data['username'])
    return user, moderator


def create_non_verify_user(user_client):
    # для письма

    data = {
        'username': 'TestUser5000',
        'email': 'testuser44@gmail.fake',
        'password': 'verDen134',
    }
    user_client.post('/api/v1/auth/signup/', data=data)
    user = get_user_model().objects.get(email=data['email'])
    return user


def auth_client(user):
    token, _ = Token.objects.get_or_create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client


def auth_client_by_token(token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    return client


def parser_verify_link(body):
    email_lines = body.splitlines()
    activation_link = [url for url in email_lines if '/email-verify/' in url]

    try:
        uid, token = activation_link[0].split("/")[-2:]
    except ValueError:
        return False
    return uid, token


def parser_reset_link(body):
    email_lines = body.splitlines()
    activation_link = [url for url in email_lines if '/reset-password/' in url]
    try:
        uid, token = activation_link[0].split("/")[-2:]
    except ValueError:
        return False
    return uid, token
