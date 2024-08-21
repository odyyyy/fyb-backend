from django.contrib import admin

from vacancies.forms import MusicianVacancyForm, BandVacancyForm
from vacancies.models import MusicianVacancy, BandVacancy, OrganizerVacancy


class MusicianVacancyAdmin(admin.ModelAdmin):
    form = MusicianVacancyForm


class BandVacancyAdmin(admin.ModelAdmin):
    form = BandVacancyForm


admin.site.register(MusicianVacancy, MusicianVacancyAdmin)
admin.site.register(BandVacancy, BandVacancyAdmin)
admin.site.register(OrganizerVacancy)
