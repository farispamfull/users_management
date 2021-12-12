# Users management
[![users_management workflow](https://github.com/farispamfull/users_management/actions/workflows/users_management.yml/badge.svg)](https://github.com/farispamfull/users_management/actions/workflows/users_management.yml)
* [Техническое задание](#tech-task)
* [Описание проекта](#description)
* [Процесс регистрации](#registations)
* [Сброс пароля](#reset_password)
* [API](#api)
* [Локальный запуск](#dev)


## Техническое задание <a name="tech-task"></a>

Сделайте CRUD для юзеров с токен аутентификацией. Для примера можно взять https://emphasoft-test-assignment.herokuapp.com/swagger/ 
Опционально: тесты, линтер и статическая типизация

## Описание проекта <a name="description"></a>

Так как в задании не говорится о контексте и присутствует только crud, принял решение 
реализовать на низком уровне контроль над пользователями и их аутентификацией
без использования сторонних библиотек

* В проекте есть роли: `moderator` `admin` `user`
 
  * admin - полные права, может удалять и создавать пользователей, приписывать им роли и статус верификации
  * moderator - прав на данном этапе нет, потому что других приложений кроме юзера нет
  * user - аутентифицированный пользователь. При регистрации каждый получает этот статус

* Реализованы сброс пароля и верификация email

  * Два раза использовать одну и ту же ссылку при удачном сбросе или верификации нельзя

* Написаны тесты с хорошим покрытием

## Процесс регистрации <a name="registations"></a>
1. Пользователь отправляет post запрос с параметрами  `email`,`username`,`password` на `/api/v1/auth/signup/`.
2. Далее пользователь приходит письмо с ссылкой на подтверждение email.
пользователь оправляет post запрос с параметрами `uid`,`token` на `api/v1/auth/email-verify/` для подтверждения
3. Далее пользователь отправляет post запрос с параметрами  `email`, `password` на `/api/v1/auth/token/login/`.
В ответ ему приходит **токен** 

* При желании юзер может посмотреть или изменить свои данные (профиль) на `/api/v1/users/me/`
* Для выхода из системы get запрос на `api/v1/auth/token/logout/`

## Процесс сброса пароля <a name="reset_paasword"></a>
1. Пользователь отправляет post запрос с параметрами `email` на `api/v1/auth/reset-password/`
2. Пользователю приходит письмо ссылкой на смену пароля. Пользователь отправляет
post запрос с параметрами на `uid`,`token`,`new_password``api/v1/auth/reset-password/confirm/`

## API
```
Prefix /api/v1/

users/
  - get (permissions: authentication)
  - post (permissions: admin)

users/:id/
  - get (permissions: admin)
  - delete (permissions: admin)
  - path (permissions: admin)

users/me/
  - get (permissions: authentication)
  - patch (permissions: authentication)
```

```
Prefix /api/v1/auth/

token/login/
  - post

token/logout/
  - get

email-verify/
  - post

reset-password/
  - post

reset-password/confirm/
  - post

```

## Локальный запуск Docker <a name="dev"></a>
Создайте файл .env и поместите в корневой каталог проекта

Запишите в нем переменные окружения:
```
DEBUG=False
SECRET_KEY=Сгенерируйте ключ
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgresql
POSTGRES_USER=postgresql
POSTGRES_PASSWORD=postgresql
DB_HOST=db
DB_PORT=5432
```
запустите docker-compose:
```
 docker-compose -f docker-compose.yaml -f docker-compose-dev.yaml up -d
```

При первом запуске выполнить миграции:

```
docker-compose exec web python manage.py makemigration
docker-compose exec web python manage.py migrate
```

Соберите статику:
```
docker-compose exec web python manage.py collectstatic --no-input