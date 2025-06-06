# users/admin.py

from django.contrib import admin
from django.utils.html import format_html

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "role", "is_staff", "get_avatar")
    list_filter = ("role",)
    search_fields = ("email", "username")

    def get_avatar(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" style="border-radius: 50%;">', obj.avatar.url)
        return "—"

    get_avatar.short_description = "Аватар"
