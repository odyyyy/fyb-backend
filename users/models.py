import enum

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_MUSICIAN_ROLE = (('musician', 'Musician'),
                          ('band', 'Band'),
                          ('organizer', 'Organizer'))

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
