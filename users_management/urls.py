from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

]
