from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name',
                  'username', 'bio', 'email', 'role')
        model = User





