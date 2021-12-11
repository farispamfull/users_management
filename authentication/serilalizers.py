from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from authentication.utils import decode_uid

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username')
        extra_kwargs = {'password': {'write_only': True,
                                     'validators': [validate_password]}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        validators=[validate_password],
        required=True)
    password2 = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)

    def validate(self, data):
        old_password = data['old_password']
        user = self.context['request'].user

        if not user.check_password(old_password):
            raise serializers.ValidationError(
                {"old_password": "Wrong password"})
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password2": "Password fields didn't match."})
        return data


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = authenticate(password=password, email=email)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        if not user.is_verified:
            raise serializers.ValidationError('Email is not verified')

        if not user.is_active:
            raise serializers.ValidationError(
                'Account disabled, contact admin')
        self.user = user
        return data


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField()

    class Meta:
        model = Token


class UidTokenSerilaizer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        try:
            user_id = decode_uid(attrs.get('uid'))
            self.user = User.objects.get(id=user_id)
        except Exception as e:
            raise serializers.ValidationError('invalid uid code')

        if not default_token_generator.check_token(self.user,
                                                   attrs.get('token')):
            raise serializers.ValidationError('invalid token')
        return attrs


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.SlugRelatedField(
        slug_field='email', queryset=User.objects.all())

    class Meta:
        model = User
        fields = ('email',)
