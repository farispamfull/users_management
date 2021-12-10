from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import MyUserChangeForm, CustomUserCreationForm
from .models import User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = CustomUserCreationForm
    model = User

    list_display = (
        'email', 'username', 'is_staff', 'is_verified', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'),
         {'fields': ('username', 'first_name', 'last_name', 'bio')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified',
                       'role', 'groups',
                       'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(User, MyUserAdmin)
