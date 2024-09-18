from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model

@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'first_name', 'last_name',
              'image', 'is_staff', 'is_active', 'last_login')




