from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication import utils
from .serilalizers import (UserRegistrationSerializer, UserLoginSerializer,
                           UidTokenSerilaizer, ResetPasswordSerializer,
                           ResetPasswordConfirmSerializer)
from .utils import (send_token_for_email, send_reset_password_for_email,
                    logout_user)

User = get_user_model()


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        send_token_for_email(self.request, user)


class EmailVerifyView(APIView):

    def post(self, request):
        serializer = UidTokenSerilaizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.user.is_verified = True

        if hasattr(serializer.user, 'last_login'):
            serializer.user.last_login = now()

        serializer.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = utils.login_user(request, serializer.user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.data.get('email'))
        send_reset_password_for_email(request, user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConfirmResetPassword(APIView):

    def post(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.user.set_password(serializer.data.get('new_password'))

        if hasattr(serializer.user, 'last_login'):
            serializer.user.last_login = now()

        if hasattr(serializer.user, 'auth_token'):
            serializer.user.auth_token.delete()
        serializer.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout_user(request)
    return Response(status=status.HTTP_204_NO_CONTENT)
