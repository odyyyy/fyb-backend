from django.db import models

from vacancies.models.base import FavouritesMixin, Vacancy


class OrganizerVacancy(Vacancy, FavouritesMixin):
    title = models.CharField(max_length=255, verbose_name="Название")
    event_type = models.CharField(max_length=255, verbose_name="Тип мероприятия")
    address = models.CharField(max_length=255, verbose_name="Адрес мероприятия")
    event_datetime = models.DateTimeField(verbose_name="Время мероприятия")

    class Meta:
        verbose_name = "Объявление организатора"
        verbose_name_plural = "Объявления организаторов"

    def __str__(self):
        return self.title
