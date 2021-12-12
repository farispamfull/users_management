import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from .common import (create_non_verify_user, parser_verify_link,
                     create_users_api,
                     auth_client_by_token, parser_reset_link)


class Test02AuthAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_users_post_signup(self, client, user_client, admin):
        data = {}
        response = client.post('/api/v1/auth/signup/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/auth/signup/` с не правильными данными возвращает 400'
        )
        data = {
            'username': 'TestUser1231231',
            'password': 'SasasS18',
            'email': admin.email
        }
        response = client.post('/api/v1/auth/signup/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/auth/signup/` с не правильными данными возвращает 400. '
            '`Email` должен быть уникальный у каждого прользователя'
        )
        data = {
            'username': admin.username,
            'password': 'SasasS181',
            'email': 'testuser@gmail.fake'
        }
        response = client.post('/api/v1/auth/signup/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/auth/signup/` с не правильными данными возвращает 400. '
            '`Username` должен быть уникальный у каждого прользователя'
        )
        data = {'username': 'Testuser3789',
                'password': 'SasasS18',
                'email': 'test@gmail.fake'}
        response = client.post('/api/v1/auth/signup/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/v1/auth/signup/` с правильными данными возвращает 201.'
        )
        assert response.data.get('username') == data['username'], (
            'Проверьте, что при POST запросе `/api/v1/auth/signup/` с правильными данными возвращаете `username`.'
        )
        assert response.data.get('email') == data['email'], (
            'Проверьте, что при POST запросе `/api/v1/auth/signup/` с правильными данными возвращаете `email`.'
        )
        assert len(response.data) == 2, (
            'Проверьте, что при POST запросе `/api/v1/auth/signup/` с правильными данными возвращаетcя только `email` и username'
        )
        assert get_user_model().objects.count() == 2, (
            'Проверьте, что при POST запросе `/api/v1/auth/signup/` вы создаёте пользователей.'
        )
        assert get_user_model().objects.get(
            email=data['email']).is_verified is False, (
            'Проверьте, что при POST запросе `/api/v1/auth/signup/` вы создаёте пользователей c не подтвержденным email.'
        )
        assert len(mail.outbox) == 1, (
            'Проверьте, что при POST запросе `/api/v1/auth/signup/ вы отправляете письмо с ссылкой на потверждение email'

        )

    @pytest.mark.django_db(transaction=True)
    def test_02_users_get_signup(self, client):
        response = client.get('/api/v1/auth/signup/')
        assert response.status_code == 405, (
            'Проверьте, что при GET запросе `/api/v1/auth/signup/` возвращается статус 405'
        )

        response = client.patch('/api/v1/auth/signup/')
        assert response.status_code == 405, (
            'Проверьте, что при PATCH запросе `/api/v1/auth/signup/` возвращается статус 405'
        )
        response = client.delete('/api/v1/auth/signup/')
        assert response.status_code == 405, (
            'Проверьте, что при DELETE запросе `/api/v1/auth/signup/` возвращается статус 405'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_users_email_verify_link(self, user_client):
        user = create_non_verify_user(user_client)
        body = mail.outbox[0].body
        assert 'auth/email-verify/' in body, (
            'Проверьте, что письмо подтверждения email отправляется с правильной ссылкой на потверждение'
        )

        uid, token = parser_verify_link(mail.outbox[0].body)
        assert default_token_generator.check_token(user, token) == True, (
            'Проверьте, что письмо подтверждения email отправляется с правильным токеном'
        )
        assert force_str(urlsafe_base64_decode(uid)) == str(user.id), (
            'Проверьте, что письмо подтверждения email отправляется с правильным uid'
        )

    @pytest.mark.django_db(transaction=True)
    def test_04_users_email_verify(self, client):
        user = create_non_verify_user(client)
        uid, token = parser_verify_link(mail.outbox[0].body)
        data = {}
        response = client.post('/api/v1/auth/email-verify/',
                               data=data)
        assert response.status_code == 400, (
            'Проверить, что при POST запросе /api/v1/users/auth/email-verify/'
            'c не правильными данными возвращается статус 400'
        )
        data = {
            'uid': 'WR',
            'token': 'wrongToken'
        }
        response = client.post('/api/v1/auth/email-verify/',
                               data=data)
        assert response.status_code == 400, (
            'Проверить, что при POST запросе /api/v1/users/auth/email-verify/'
            'c не правильными данными возвращается статус 400'
        )
        data = {
            'uid': uid,
            'token': token
        }
        response = client.post('/api/v1/auth/email-verify/',
                               data=data)
        assert response.status_code == 204, (
            'Проверить, что при POST запросе /api/v1/users/auth/email-verify/'
            'c правильными данными возвращается статус 204'
        )
        status = get_user_model().objects.get(email=user.email).is_verified
        assert status is True, (
            'Проверить, что при POST запросе /api/v1/users/auth/email-verify/'
            'статус email юзера поменялся на True'
        )

    @pytest.mark.django_db(transaction=True)
    def test_04_users_login(self, client, user_client):
        user, moderator = create_users_api(user_client)
        data = {}
        response = client.post('/api/v1/auth/token/login/',
                               data=data)
        assert response.status_code == 400, (
            'Проверить, что при POST запросе /api/v1/auth/token/login/'
            'c не правильными данными возвращается статус 400'
        )
        data = {'email': 'wrong@gmail',
                'password': 'wrTfgh'}
        response = client.post('/api/v1/auth/token/login/',
                               data=data)
        assert response.status_code == 400, (
            'Проверить, что при POST запросе /api/v1/auth/token/login/'
            'c не правильными данными возвращается статус 400'
        )
        data = {'email': 'wrong@gmail',
                'password': 'wrTfgh'}
        response = client.post('/api/v1/auth/token/login/',
                               data=data)
        assert response.status_code == 400, (
            'Проверить, что при POST запросе /api/v1/auth/token/login/'
            'c не правильными данными возвращается статус 400'
        )

        user.set_password('test24gd')
        user.save()
        data = {'email': user.email,
                'password': 'test24gd'}
        response = client.post('/api/v1/auth/token/login/',
                               data=data)

        assert response.status_code == 400, (
            'Проверить, что при POST запросе /api/v1/users/auth/token/login/'
            'c не подтвержденным email возвращается статус 400'
        )
        moderator.set_password('test24gd')
        moderator.save()
        data = {'email': moderator.email,
                'password': 'test24gd'}
        response = client.post('/api/v1/auth/token/login/', data=data)
        assert response.status_code == 200, (
            'Проверить, что при POST запросе /api/v1/users/auth/token/login/'
            'c подтвержденным email возвращается статус 200'
        )
        data = {'email': moderator.email,
                'password': 'test24gd'}
        response = client.post('/api/v1/auth/token/login/', data=data)

        assert response.data.get('token', None) != None, (
            'Проверить, что при POST запросе /api/v1/users/auth/token/login/'
            'c подтвержденным email возвращается token'
        )

        data = {'email': moderator.email,
                'password': 'test24gd'}
        response = client.post('/api/v1/auth/token/login/', data=data)
        token = response.data.get('token')
        auth_client = auth_client_by_token(token)
        response = auth_client.get('/api/v1/users/me/')
        assert response.status_code == 200, (
            'Проверить, что при POST запросе /api/v1/users/auth/token/login/'
            'c подтвержденным email возвращается верный auth токен'
        )
        assert response.data.get('email') == data['email'], (
            'Проверить, что при POST запросе /api/v1/users/auth/token/login/'
            'c подтвержденным email возвращается верный auth токен'
        )

    @pytest.mark.django_db(transaction=True)
    def test_05_users_reset_password(self, client, user_client):
        user, moderator = create_users_api(user_client)
        data = {}
        response = client.post('/api/v1/auth/reset-password/',
                               data=data)
        assert response.status_code == 400, (
            'Проверить, что при POST запросе /api/v1/auth/reset-password/'
            'c не правильными данными возвращается статус 400'
        )

        data = {'email': 'wrong@gmail.com'}
        response = client.post('/api/v1/auth/reset-password/',
                               data=data)
        assert response.status_code == 400, (
            'Проверить, что при POST запросе /api/v1/auth/reset-password/'
            'c не правильными данными возвращается статус 400'
        )

        data = {'email': moderator.email}
        response = client.post('/api/v1/auth/reset-password/',
                               data=data)
        assert response.status_code == 204, (
            'Проверить, что при POST запросе /api/v1/auth/reset-password/'
            'c правильными данными возвращается статус 204'
        )
        assert len(mail.outbox) == 1, (
            'Проверить, что при POST запросе /api/v1/auth/reset-password/'
            'с правильными данными, отправялется письмо'
        )

    @pytest.mark.django_db(transaction=True)
    def test_05_users_reset_password_link(self, client, user_client):
        user, moderator = create_users_api(user_client)

        client.post('/api/v1/auth/reset-password/',
                    data={'email': moderator.email})

        body = mail.outbox[0].body
        assert 'reset-password/confirm/' in body, (
            'Проверьте, что письмо на изменение пароля отправляется с правильной ссылкой на изменение'
        )

        uid, token = parser_reset_link(mail.outbox[0].body)
        assert default_token_generator.check_token(moderator, token) == True, (
            'Проверьте, что письмо на изменение пароля отправляется с верным токеном'
        )
        assert force_str(urlsafe_base64_decode(uid)) == str(moderator.id), (
            'Проверьте, что письмо письмо на изменение пароля отправляется с правильным uid'
        )

    @pytest.mark.django_db(transaction=True)
    def test_06_users_reset_password_confirm(self, client, user_client):
        user, moderator = create_users_api(user_client)
        client.post('/api/v1/auth/reset-password/',
                    data={'email': moderator.email})

        data = {}
        response = client.post('/api/v1/auth/reset-password/confirm/',
                               data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на api/v1/auth/reset-password/confirm/'
            'c не правильными данными возвращается статус 400'
        )
        data = {
            'uid': 'AA',
            'token': 'Wrongt54',
            'new_password': 'Sandt14Df'
        }
        response = client.post('/api/v1/auth/reset-password/confirm/',
                               data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на api/v1/auth/reset-password/confirm/'
            'c не правильными данными возвращается статус 400'
        )
        uid, token = parser_reset_link(mail.outbox[0].body)
        data = {
            'uid': uid,
            'token': token,
            'new_password': 'Sandt14Df'
        }
        response = client.post('/api/v1/auth/reset-password/confirm/',
                               data=data)
        assert response.status_code == 204, (
            'Проверьте, что при POST запросе на api/v1/auth/reset-password/confirm/'
            'c правильными данными возвращается статус 400'
        )

        user = get_user_model().objects.get(email=moderator.email)
        assert user.check_password(data['new_password']) is True, (
            'Проверьте, что POST запрос на api/v1/auth/reset-password/confirm/'
            'c правильными данными изменяет пароль юзера'
        )
