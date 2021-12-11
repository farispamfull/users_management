from django.urls import include, path
from rest_framework.routers import DefaultRouter

from authentication.views import (UserRegistrationView, UserLoginView,
                                  user_logout, EmailVerifyView,
                                  ResetPasswordView, ConfirmResetPassword)
from users.views import UserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')

auth_patterns = [path('signup/', UserRegistrationView.as_view()),
                 path('token/login/', UserLoginView.as_view()),
                 path('token/logout/', user_logout),
                 path('email-verify/', EmailVerifyView.as_view()),
                 path('reset-password/', ResetPasswordView.as_view()),
                 path('reset-password/confirm/',
                      ConfirmResetPassword.as_view()),

                 ]

urlpatterns = [path('v1/auth/', include(auth_patterns)),
               path('v1/', include(router_v1.urls)), ]
