from django.contrib import admin

from vacancies.forms import MusicianVacancyForm, BandVacancyForm
from vacancies.models import MusicianVacancy, BandVacancy, OrganizerVacancy

@admin.register(MusicianVacancy)
class MusicianVacancyAdmin(admin.ModelAdmin):
    form = MusicianVacancyForm

@admin.register(BandVacancy)
class BandVacancyAdmin(admin.ModelAdmin):
    form = BandVacancyForm


admin.site.register(OrganizerVacancy)
