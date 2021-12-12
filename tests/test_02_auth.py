import pytest
from django.contrib.auth import get_user_model
from django.core import mail


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
