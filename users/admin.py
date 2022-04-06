from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class UserAdmin(UserAdmin):
    """ Custom User Admin """

    custom_fieldsets = (
        ('Custom', {
            "fields": (
                'avatar',
                'birthdate',
                'superhost',
            ),
        }),
    )

    fieldsets = UserAdmin.fieldsets + custom_fieldsets

    list_filter = UserAdmin.list_filter + ('superhost',)

    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'is_active',
        'superhost',
        'is_staff',
        'is_superuser',
    )
