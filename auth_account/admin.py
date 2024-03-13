from django.contrib import admin
from .models import CustomUser, ProfilePicture
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    list_display = ["id", "email", "first_name", "last_name", "is_admin"]
    list_filter = [
        "is_admin",
    ]
    list_editable = [
        "is_admin",
    ]
    list_per_page = 10
    fieldsets = [
        ("CropShield User's Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ],
            },
        ),
    ]
    search_fields = ["first_name__startswith", "last_name__startswith"]
    ordering = [
        "id",
        "first_name",
        "last_name",
    ]
    filter_horizontal = []


"""Need to work on bellow"""
admin.site.register(CustomUser, UserAdmin)


admin.site.register(ProfilePicture)
