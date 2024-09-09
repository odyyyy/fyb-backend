import uuid
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from bands.models import Band


class VacancyQuerySet(models.QuerySet):
    def with_related(self):
        return self.select_related('created_by').prefetch_related('favourites').order_by('-created_at')


class Vacancy(models.Model):
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Автор")
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name="Описание")
    uuid = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    objects = VacancyQuerySet.as_manager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.created_by.username + ' - ' + str(self.uuid)


INSTRUMENTS = [
    ('guitar', 'Guitar'),
    ('bass', 'Bass'),
    ('drums', 'Drums'),
    ('piano', 'Piano'),
    ('other', 'Other'),
]

SKILL_LEVELS = [
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
]

GENRES = [
    ('rock', 'Rock'),
    ('pop', 'Pop'),
    ('jazz', 'Jazz'),
    ('classical', 'Classical'),
    ('metal', 'Metal'),
    ('electronic', 'Electronic'),
    ('other', 'Other'),
]


class FavouritesMixin(models.Model):
    favourites = models.ManyToManyField(
        get_user_model(),
        related_name="%(class)s_favourites",
        blank=True,
        verbose_name="Избранное"
    )

    class Meta:
        abstract = True


class BaseMusicVacancy(Vacancy, FavouritesMixin):
    genres = ArrayField(models.CharField(max_length=50, choices=GENRES), size=3, default=list, verbose_name="Жанры")
    level = models.CharField(choices=SKILL_LEVELS, max_length=50, verbose_name="Уровень игры")
    city = models.CharField(max_length=50, verbose_name="Город")
    contacts = ArrayField(models.CharField(max_length=100), size=3, verbose_name="Контакты")

    class Meta:
        abstract = True


class MusicianVacancy(BaseMusicVacancy):
    instruments = ArrayField(
        models.CharField(max_length=50, choices=INSTRUMENTS),
        size=3,
        default=list,
        verbose_name="Инструменты"
    )

    class Meta:
        verbose_name = "Объявление музыканта"
        verbose_name_plural = "Объявления музыкантов"


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
