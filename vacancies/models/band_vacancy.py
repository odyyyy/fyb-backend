from django.db import models

from bands.models import Band
from vacancies.models.base import GENRES, INSTRUMENTS, BaseMusicVacancy


class BandVacancy(BaseMusicVacancy):
    created_by = models.OneToOneField(Band, on_delete=models.CASCADE, related_name='band_vacancy',
                                      verbose_name="Группа")
    instrument = models.CharField(max_length=50, choices=INSTRUMENTS, verbose_name="Инструмент")
    genres = models.CharField(max_length=50, choices=GENRES, verbose_name="Жанр")

    class Meta:
        verbose_name = "Объявление группы"
        verbose_name_plural = "Объявления групп"

    def __str__(self):
        return f'{self.created_by.name} want to find - {str(self.instrument).capitalize()} player'
