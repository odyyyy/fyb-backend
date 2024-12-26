import uuid
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models

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

INSTRUMENTS = [
    ('guitar', 'Guitar'),
    ('bass', 'Bass'),
    ('drums', 'Drums'),
    ('piano', 'Piano'),
    ('other', 'Other'),
]


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
