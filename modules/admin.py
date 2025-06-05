from django.contrib import admin

from .models import Module


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    list_filter = ("author",)
    search_fields = ("title", "description")
