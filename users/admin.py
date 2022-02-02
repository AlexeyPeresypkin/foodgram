from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

admin.site.unregister(User)


@admin.register(User)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',)
    list_filter = UserAdmin.list_filter + (
        'email', 'username', "first_name", "last_name",
    )
    search_fields = UserAdmin.search_fields
    ordering = UserAdmin.ordering
