from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        fields = ('email', 'username')
        model = User


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        fields = ('email', 'username')
        model = User
