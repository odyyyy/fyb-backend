from django.contrib import admin

from bands.models import Band


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    list_filter = ('name',)
    search_fields = ('name', 'city')
