from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from core.web.models.ballot import Ballot
from core.web.models.log import Log
from core.web.models.user import User


@admin.register(User)
class UserAdmin(UserAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ["passport", "email",]
        return []

    list_display = ("passport", "email", "is_active",)
    fieldsets = (
        (None, {
            "fields": (
                "passport", "password", "email", "is_active",
            )
        }),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("passport", "email", "password1", "password2")
            }
        ),
    )
    filter_horizontal = ()
    list_filter = ()
    readonly_fields = ("passport", "email",)
    ordering = ("passport",)


@admin.register(Ballot)
class BallotAdmin(ModelAdmin):

    list_display = ("address",)
    readonly_fields = ("address",)
    ordering = ("address",)


@admin.register(Log)
class LogAdmin(ModelAdmin):

    list_display = ("created_at", "user", "action", "location",)
    fieldsets = (
        (None, {
            "fields": (
                "created_at", "user", "action", "location",
            )
        }),
    )
    readonly_fields = ("created_at", "user", "action", "ip", "location",)


admin.site.unregister(Group)
