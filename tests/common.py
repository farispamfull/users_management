from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


def create_users_api(user_client):
    data = {
        'username': 'TestUser1234',
        'role': 'user',
        'email': 'testuser@gmail.fake'
    }
    user_client.post('/api/v1/users/', data=data)
    user = get_user_model().objects.get(email=data['email'])
    data = {
        'first_name': 'fsdfsdf',
        'last_name': 'dsgdsfg',
        'username': 'TestUser4321',
        'bio': 'Jdlkjd',
        'role': 'moderator',
        'email': 'testuser2342@gmail.fake'
    }
    user_client.post('/api/v1/users/', data=data)
    moderator = get_user_model().objects.get(username=data['username'])
    return user, moderator


def auth_client(user):
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client
