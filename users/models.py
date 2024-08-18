import enum

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

USER_MUSICIAN_ROLE = [('musician', 'Nusician'), ('band', 'Band'), ('organizer', 'Organizer')]


class User(AbstractUser):
    role = models.CharField(max_length=50, choices=USER_MUSICIAN_ROLE, default='musician', verbose_name="Роль")
    image = models.ImageField(upload_to='media/photos/users/%Y/%m/%d/', blank=True, null=True, verbose_name="Фото")
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True
    )


class Band(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")
    members = models.ManyToManyField(get_user_model(), related_name='band_members', verbose_name="Участники")
    leader = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='band_leader', verbose_name="Лидер")
    city = models.CharField(max_length=50, verbose_name="Город")
    image = models.ImageField(upload_to='media/photos/bands/%Y/%m/%d/', blank=True, null=True, verbose_name="Фото")

    class Meta:
        verbose_name = "Музыкальная группа"
        verbose_name_plural = "Музыкальные группы"

    def __str__(self):
        return self.name
