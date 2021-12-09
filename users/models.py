from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserRoles(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    role = models.CharField(max_length=10, blank=True,
                            choices=UserRoles.choices, default=UserRoles.USER)
    first_name = models.CharField(
        max_length=150, verbose_name='First name')
    last_name = models.CharField(
        max_length=150, verbose_name='Last name')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, )
    last_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
