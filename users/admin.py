from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import Band


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    list_filter = ('role',)
    search_fields = ('username', 'email')


admin.register(get_user_model(), UserAdmin)
admin.site.register(Band)
