from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserRoles(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class User(AbstractUser):
    email = models.EmailField(_('email'), max_length=254, unique=True,
                              db_index=True)
    role = models.CharField(_('role'), max_length=10, blank=True,
                            choices=UserRoles.choices, default=UserRoles.USER)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=50, unique=True)
    bio = models.TextField(_('description'), blank=True, )
    is_verified = models.BooleanField(_('verified'), default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_admin(self):
        return (self.role == UserRoles.ADMIN
                or self.is_staff or self.is_superuser)

    @property
    def is_moderator(self):
        return self.role == UserRoles.MODERATOR

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['username']
