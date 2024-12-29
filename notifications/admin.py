from django.contrib import admin

from notifications.models import NotificationSubscription


@admin.register(NotificationSubscription)
class NotificationAdmin(admin.ModelAdmin):
    pass
